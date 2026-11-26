# Change Log

## 2.2.0 - 2026-11-26

**Web UI**
- Professional redesign across the admin (`assets/css/hodi-theme.css`): Inter type scale, one card/table/button/form system, white grouped sidebar, sticky top bar with facility search, one primary action per page, WCAG AA colours, visible focus, responsive to 375px. New dashboard (key numbers, "needs attention", quick actions). Facility list/form, documents, music, users, sign-in and password pages reworked.
- New public landing page: quick-exit button (Esc twice), emergency numbers (1195, 999/112, 116, GVRC), how it works, live coverage from the directory (top counties, services, GBV categories; cached 15 min), the app, privacy and safety, FAQ, contact; one footer; Open Graph tags.
- Branded 403/404/500 pages that are now actually used (handlers in `core/errors.py`; the 500 page needs no database).
- Fixed: every `.alert` was turned into a disappearing toast (form errors, delete warnings, SMS banners); sign-in errors vanished after a second; Bootstrap 5 popups on a Bootstrap 4 page on the facility form; notification script retried WebSockets 5x per page and stacked duplicate poll timers.

**Backend**
- Errors: the app and API always get JSON `{"error": ...}` (DRF `EXCEPTION_HANDLER` + 404/500 handlers); 82 places that sent exception text to users now show a clear message and log the traceback; debug `print`s replaced by logging.
- Facility create/edit: a failing infrastructure row no longer breaks the facility's transaction silently (own savepoint + warning).
- Users: self-registration off by default (`ALLOW_SELF_REGISTRATION`); new **Add user** page (`/users/new/`, permission `add_users`) - the person gets a one-time set-password link by email and SMS.
- Removed the hard-coded Google Maps key default.
- `manage.py repair_contacts [--apply]`: fixes the 34 broken phone contacts from imports (junk digits off, glued landline+mobile split, labelled text, email stored as phone); nothing deleted.
- Repo tidy: docs in `docs/`, one-off tools in `scripts/` (not collected by pytest), logs/exports untracked; README rewritten.
- Mail: production sends as `Hodi <no-reply@hodi-admin.co.ke>` through the local mail server.

## 2.1.0 - 2026-11-25

- **Chat alerts by SMS (Bonga).** The staff member a help chat is assigned to gets a text; on-call numbers get one when a new chat starts and when the app marks a message urgent. Texts carry only the chat number and link, never what the person wrote. Switches and on-call numbers on SMS settings, with a list of recent alerts. Each alert goes once per chat and phone (`sms_notifications` table, migration `sms.0003`).
- **Privacy:** the chat service printed the first 100 characters of every message into the server log; removed, and its other debug prints now go to `logger.debug`.
- **`manage.py check_data`:** read-only consistency report (geography duplicates, facility locations outside Kenya or at 0,0, missing locations/contacts/categories, bad contact numbers, users without roles, missing uploaded files, SMS configuration). `--strict` exits 1 on errors.
- **Production settings:** `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` read the server's `.env` (they were ignored, so switching the server to prod settings would have refused hodi-admin.co.ke); log file rotates at 10 MB x 5 (logs/ had grown past 300 MB); `DEFAULT_FROM_EMAIL` defaults to the SMTP account; `SITE_URL` setting; `DJANGO_ENV` is read from `.env`.

## [2.0.0] 2026-11-24
### Platform
- Python 3.15.2 and Django 6.1.3 (was Python 3.12 / Django 4.2); DRF 3.18,
  Pillow 13, gunicorn 27, psycopg 3. Unused packages dropped; test and debug
  tools moved to `requirements-dev.txt`.
- `STORAGES` replaces the removed `STATICFILES_STORAGE`; `MAILERS` replaces
  the deprecated `EMAIL_*` settings; drf-yasg schema URLs use the new format.
- `core.settings.test`: the suite runs on in-memory SQLite whatever `.env` says.

### New
- Bulk SMS (`apps.sms`) through the Intelli-Wealth Bonga account, like
  IntelliCash: facility contacts by county/constituency/ward/GBV service,
  staff by role, typed numbers; live recipient and cost preview, background
  sending with progress, retry, stop, test SMS, write-only credentials, and
  `view_sms` / `send_sms` / `change_sms` permissions.
- Map Settings: OpenStreetMap or Google Maps for the facility map, the new
  facility location picker (address search + click/drag pin) and the mobile
  app (`GET /mobile/config/map/`).

### Fixed
- Settings fields dropped from the model in July but still in the database
  (inserts would fail) are back; models and migrations agree again.
- `/api/facilities/`, `/api/facilities/search/`, `/api/facilities/map/` and the
  emergency/GBV/referral searches crashed (wrong relation names, distinct after
  slice). The facility map no longer runs one query per facility or 500s on a
  bad `zoom`/bounds value, and escapes facility names.
- `collectstatic` aborted on missing source maps and theme images.
- Theme colours from Settings never applied (invalid JSON in the base layout).
- Bootstrap was loaded twice, once blocked by a wrong integrity hash.
- Chat notifications polled a URL that does not exist.
- Any logged-in account could change Application Settings; it now needs
  `change_settings`.

### Security (found by the new test suite)
- **Chat**: the admin chat API had no permission check and four chat pages no
  login check, so anyone could list GBV conversations, read and export
  transcripts and change their status. All now need signed-in staff with
  `view_chat` (`change_chat` for changes); staff replies are attributed.
- Services, Human Resources and Infrastructure pages were open to anonymous
  visitors; they need `view_facilities`. User detail needs `view_users`.
- Login followed any `?next=` URL (open redirect); now same-site only.
- Geography add/edit/delete were CSRF-exempt; now CSRF-protected.
- Password reset never worked (placeholder) and told visitors which emails
  have accounts. It now emails a signed, single-use link to the account owner
  and answers the same for unknown addresses.
- Production refuses to start with the placeholder `SECRET_KEY`.
- The mobile documents list served private documents.
- The Gemini key moved from the request URL (which reached logs) to a header;
  the chat API no longer returns tracebacks.

### Fixed (also found by the tests)
- Facilities could not be created or edited from the dashboard (user id given
  where a user was needed; cache clean-up crashed inside the save); only one
  facility could leave its code blank; coordinates had no range check.
- Role assignments with a future expiry date were treated as expired.
- Profile form, document delete, music play tracking and duration, chat
  analytics date range and export, admin conversation list, mobile photo/voice
  uploads, session location, AI history parsing, API search by POST and
  unknown-contact 404 all crashed or misbehaved.
- Legacy pages (/icons/, /tables/...) always served a fake 404 with status 200.

## [1.0.1] 2024-01-25
### Changes

- Pin versions in `req.txt`

## [1.0.0] 2023-04-09
### Initial Release

- Code the basic structure

