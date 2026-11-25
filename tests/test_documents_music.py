"""
Documents (/documents/) and music (/music/) dashboard views, forms and models.
"""

import datetime
import json

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from apps.documents.forms import DocumentForm, DocumentUploadForm
from apps.documents.models import Document
from apps.music.forms import MusicForm
from apps.music.models import Music, MusicPlay
from tests.conftest import grant, logged_in_client

pytestmark = pytest.mark.django_db


@pytest.fixture
def editor(staff_user):
    grant(staff_user, "view_documents", "add_documents", "change_documents",
          "delete_documents", "view_music", "add_music", "change_music")
    return staff_user


@pytest.fixture
def editor_client(editor):
    return logged_in_client(editor)


def make_doc(user, lookups, **kw):
    data = dict(title="Safety plan", document_type=lookups["doc_type"], uploaded_by=user,
                content="Steps", is_public=True)
    data.update(kw)
    return Document.objects.create(**data)


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

class TestDocumentViews:
    def test_login_required(self, client):
        r = client.get("/documents/")
        assert r.status_code == 302 and "/login/" in r["Location"]

    def test_list_filters_and_stats(self, editor_client, editor, lookups):
        make_doc(editor, lookups, title="Public A")
        make_doc(editor, lookups, title="Private B", is_public=False)
        make_doc(editor, lookups, title="Deleted C", is_active=False)
        r = editor_client.get("/documents/")
        assert r.status_code == 200
        assert r.context["total_documents"] == 2
        assert r.context["public_documents"] == 1 and r.context["private_documents"] == 1
        titles = lambda resp: {d.title for d in resp.context["documents"]}  # noqa: E731
        assert titles(editor_client.get("/documents/", {"search": "private"})) == {"Private B"}
        assert titles(editor_client.get("/documents/", {"is_public": "true"})) == {"Public A"}
        assert titles(editor_client.get("/documents/",
                                        {"document_type": lookups["doc_type"].pk})) == {"Public A", "Private B"}

    def test_detail(self, editor_client, editor, lookups):
        d = make_doc(editor, lookups)
        assert editor_client.get(f"/documents/{d.pk}/").context["document"] == d
        d.is_active = False
        d.save()
        assert editor_client.get(f"/documents/{d.pk}/").status_code == 404

    def test_create_with_content(self, editor_client, editor, lookups):
        r = editor_client.post("/documents/create/", {
            "title": "Know your rights", "content": "Body", "document_type": lookups["doc_type"].pk,
            "is_public": "on",
        })
        assert r.status_code == 302
        d = Document.objects.get(title="Know your rights")
        assert d.uploaded_by == editor and d.is_public

    def test_create_with_file_upload(self, editor_client, lookups):
        upload = SimpleUploadedFile("guide.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        r = editor_client.post("/documents/create/", {
            "title": "PDF guide", "document_type": lookups["doc_type"].pk, "file": upload,
        })
        assert r.status_code == 302
        d = Document.objects.get(title="PDF guide")
        assert d.file_name.endswith(".pdf")
        assert d.file_size_bytes == len(b"%PDF-1.4 test")
        assert d.get_file_extension() == ".pdf"

    def test_create_requires_some_content(self, editor_client, lookups):
        r = editor_client.post("/documents/create/", {"title": "Empty",
                                                      "document_type": lookups["doc_type"].pk})
        assert r.status_code == 200
        assert not Document.objects.filter(title="Empty").exists()

    def test_create_rejects_executable_upload(self, editor_client, lookups):
        upload = SimpleUploadedFile("evil.exe", b"MZ", content_type="application/octet-stream")
        editor_client.post("/documents/create/", {"title": "Evil",
                                                  "document_type": lookups["doc_type"].pk,
                                                  "file": upload})
        assert not Document.objects.filter(title="Evil").exists()

    def test_create_refused_without_permission(self, user_factory, lookups):
        u = user_factory(is_staff=True)
        grant(u, "view_documents")
        c = logged_in_client(u)
        r = c.post("/documents/create/", {"title": "Nope", "content": "x",
                                          "document_type": lookups["doc_type"].pk})
        assert r.status_code == 302
        assert not Document.objects.filter(title="Nope").exists()

    def test_edit(self, editor_client, editor, lookups):
        d = make_doc(editor, lookups)
        assert editor_client.get(f"/documents/{d.pk}/edit/").status_code == 200
        r = editor_client.post(f"/documents/{d.pk}/edit/", {
            "title": "Renamed", "content": "x", "document_type": lookups["doc_type"].pk,
        })
        assert r.status_code == 302
        d.refresh_from_db()
        assert d.title == "Renamed" and d.is_public is False

    def test_toggle_public(self, editor_client, editor, lookups):
        d = make_doc(editor, lookups, is_public=False)
        r = editor_client.post(f"/documents/{d.pk}/toggle-public/")
        assert r.json()["is_public"] is True
        assert editor_client.get(f"/documents/{d.pk}/toggle-public/").json()["success"] is False

    def test_delete_confirmation_page(self, editor_client, editor, lookups):
        d = make_doc(editor, lookups)
        assert editor_client.get(f"/documents/{d.pk}/delete/").status_code == 200

    def test_delete_soft_deletes_and_redirects(self, editor, lookups):
        d = make_doc(editor, lookups)
        c = Client(raise_request_exception=False)
        c.force_login(editor)
        r = c.post(f"/documents/{d.pk}/delete/")
        assert r.status_code == 302
        d.refresh_from_db()
        assert d.is_active is False

    def test_analytics(self, editor_client, editor, lookups):
        make_doc(editor, lookups)
        r = editor_client.get("/documents/analytics/")
        assert r.status_code == 200


class TestDocumentFormsAndModel:
    def test_form_requires_one_source(self, lookups):
        assert not DocumentForm(data={"title": "x", "document_type": lookups["doc_type"].pk}).is_valid()
        assert DocumentForm(data={"title": "x", "document_type": lookups["doc_type"].pk,
                                  "external_url": "https://example.org"}).is_valid()

    def test_form_respects_document_type_size_limit(self, lookups):
        lookups["doc_type"].max_file_size_mb = 0
        lookups["doc_type"].save()
        big = SimpleUploadedFile("a.pdf", b"x" * 2048, content_type="application/pdf")
        form = DocumentForm(data={"title": "x", "document_type": lookups["doc_type"].pk},
                            files={"file": big})
        assert not form.is_valid()

    def test_upload_form(self, lookups):
        ok = DocumentUploadForm(data={"title": "t", "document_type": lookups["doc_type"].pk},
                                files={"file": SimpleUploadedFile("a.txt", b"hi")})
        assert ok.is_valid()
        bad = DocumentUploadForm(data={"title": "t", "document_type": lookups["doc_type"].pk},
                                 files={"file": SimpleUploadedFile("a.sh", b"hi")})
        assert not bad.is_valid() and "file" in bad.errors

    def test_model_helpers(self, admin_user, lookups):
        d = make_doc(admin_user, lookups, file_name="old.DOCX", file_size_bytes=3 * 1024 * 1024)
        assert str(d) == "Safety plan - PDF"
        assert d.get_file_extension() == ".docx"
        assert d.get_file_size_mb() == 3.0
        assert d.get_original_filename() is None
        d.set_original_filename("../../etc/passwd")
        assert "/" not in d.get_original_filename() and ".." not in d.get_original_filename()
        plain = make_doc(admin_user, lookups, title="No file")
        assert plain.get_file_size_mb() is None and plain.get_file_extension() is None


# ---------------------------------------------------------------------------
# Music
# ---------------------------------------------------------------------------

class TestMusicViews:
    def test_login_required(self, client):
        assert client.get("/music/").status_code == 302

    def test_list_search_and_stats(self, editor_client, editor):
        a = Music.objects.create(name="Calm Waters", artist="Amani", genre="Ambient",
                                 link="https://e.org/a.mp3")
        Music.objects.create(name="Upbeat", artist="Baraka", genre="Pop", link="https://e.org/b.mp3")
        Music.objects.create(name="Hidden", is_active=False, link="https://e.org/c.mp3")
        MusicPlay.objects.create(music=a, user=editor)
        r = editor_client.get("/music/")
        assert r.context["total_tracks"] == 2 and r.context["total_listens"] == 1
        assert list(r.context["genres"]) == ["Ambient", "Pop"]
        r = editor_client.get("/music/", {"search": "calm"})
        assert [m.name for m in r.context["page_obj"]] == ["Calm Waters"]
        r = editor_client.get("/music/", {"genre": "Pop", "artist": "Baraka"})
        assert [m.name for m in r.context["page_obj"]] == ["Upbeat"]

    def test_detail_and_analytics(self, editor_client, editor):
        m = Music.objects.create(name="Calm", link="https://e.org/a.mp3", genre="Ambient")
        MusicPlay.objects.create(music=m, user=editor)
        r = editor_client.get(f"/music/{m.pk}/")
        assert list(r.context["recent_plays"])[0].music == m
        assert editor_client.get("/music/analytics/").status_code == 200
        assert editor_client.get("/music/99999/").status_code == 404

    def test_add_with_link(self, editor_client, editor):
        r = editor_client.post("/music/add/", {"name": "New", "link": "https://e.org/n.mp3"})
        m = Music.objects.get(name="New")
        assert r["Location"] == f"/music/{m.pk}/"
        assert m.created_by == editor

    def test_add_with_file(self, editor_client):
        f = SimpleUploadedFile("song.mp3", b"ID3fake", content_type="audio/mpeg")
        r = editor_client.post("/music/add/", {"name": "Uploaded", "music_file": f})
        assert r.status_code == 302
        m = Music.objects.get(name="Uploaded")
        assert m.has_file and m.music_url.endswith(".mp3")

    def test_add_requires_link_or_file(self, editor_client):
        r = editor_client.post("/music/add/", {"name": "Nothing"})
        assert r.status_code == 200
        assert not Music.objects.filter(name="Nothing").exists()

    def test_add_refused_without_permission(self, staff_client):
        staff_client.post("/music/add/", {"name": "Sneaky", "link": "https://e.org/s.mp3"})
        assert not Music.objects.filter(name="Sneaky").exists()

    def test_edit(self, editor_client, editor):
        m = Music.objects.create(name="Old", link="https://e.org/o.mp3")
        assert editor_client.get(f"/music/{m.pk}/edit/").status_code == 200
        editor_client.post(f"/music/{m.pk}/edit/", {"name": "New name", "link": "https://e.org/o.mp3"})
        m.refresh_from_db()
        assert m.name == "New name" and m.updated_by == editor

    def test_track_play_validation(self, client):
        r = client.post("/music/api/track-play/", "{}", content_type="application/json")
        assert r.status_code == 400
        assert client.get("/music/api/track-play/").status_code == 405

    def test_track_play_records_a_play(self, client, admin_user):
        m = Music.objects.create(name="Calm", link="https://e.org/a.mp3")
        r = client.post("/music/api/track-play/",
                        json.dumps({"music_id": m.pk, "user_id": admin_user.pk}),
                        content_type="application/json")
        assert r.status_code == 200
        assert MusicPlay.objects.filter(music=m).count() == 1


class TestMusicFormAndModel:
    def test_requires_link_or_file(self):
        assert not MusicForm(data={"name": "x"}).is_valid()
        assert MusicForm(data={"name": "x", "link": "https://e.org/a.mp3"}).is_valid()

    def test_rejects_non_audio_file(self):
        form = MusicForm(data={"name": "x"},
                         files={"music_file": SimpleUploadedFile("x.exe", b"MZ")})
        assert not form.is_valid() and "music_file" in form.errors

    def test_file_wins_over_link(self):
        form = MusicForm(data={"name": "x", "link": "https://e.org/a.mp3"},
                         files={"music_file": SimpleUploadedFile("a.ogg", b"OggS")})
        assert form.is_valid()
        assert form.cleaned_data["link"] == ""

    def test_duration_mm_ss(self):
        form = MusicForm(data={"name": "x", "link": "https://e.org/a.mp3", "duration": "3:30"})
        assert form.is_valid()
        assert form.cleaned_data["duration"] == datetime.timedelta(minutes=3, seconds=30)

    def test_model_properties(self, admin_user):
        m = Music.objects.create(name="Song", artist="Amani", link="https://e.org/s.mp3")
        assert str(m) == "Song - Amani"
        assert str(Music(name="Solo")) == "Solo"
        assert m.music_url == "https://e.org/s.mp3" and not m.has_file
        play = MusicPlay.objects.create(music=m, user=admin_user)
        assert m.total_listens == 1
        assert str(play).startswith("Song played by Root Admin at")
