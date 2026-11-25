from django.urls import path

from . import views

app_name = "sms"

urlpatterns = [
    path("", views.broadcast_list, name="broadcast_list"),
    path("new/", views.broadcast_compose, name="broadcast_compose"),
    path("new/preview/", views.audience_preview, name="audience_preview"),
    path("<int:broadcast_id>/", views.broadcast_detail, name="broadcast_detail"),
    path("<int:broadcast_id>/progress/", views.broadcast_progress, name="broadcast_progress"),
    path("<int:broadcast_id>/retry/", views.broadcast_retry, name="broadcast_retry"),
    path("<int:broadcast_id>/cancel/", views.broadcast_cancel, name="broadcast_cancel"),
    path("settings/", views.sms_settings, name="settings"),
    path("settings/test/", views.sms_test, name="test"),
]
