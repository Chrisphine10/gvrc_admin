# Change Log

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

