# Hodi Admin — Production Deploy Runbook

Host: `hodi-admin.co.ke` (78.159.126.22)

## 0. One-time: enable SSH key auth

Run this **from your Windows machine**. It is the only step that needs the
root password, and it removes the need for it afterwards.

```powershell
type $env:USERPROFILE\.ssh\id_ed25519_hodi_deploy.pub | ssh root@78.159.126.22 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Verify it worked (should print the hostname without prompting):

```bash
ssh -i ~/.ssh/id_ed25519_hodi_deploy root@78.159.126.22 hostname
```

Then **rotate the root password** — it has been shared in plaintext.

Once key auth works, consider disabling password login entirely:
`PasswordAuthentication no` in `/etc/ssh/sshd_config`, then
`systemctl restart sshd`. Keep an open session while testing so you cannot
lock yourself out.

## 1. Deploy

```bash
ssh -i ~/.ssh/id_ed25519_hodi_deploy root@78.159.126.22

cd /path/to/gvrc_admin          # confirm the real path first
git status                       # MUST be clean; stop if not
git pull origin main

source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput

systemctl restart gunicorn       # confirm the real service name
systemctl status gunicorn --no-pager
```

## 2. Verify (do not skip)

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://hodi-admin.co.ke/
curl -s -o /dev/null -w '%{http_code}\n' https://hodi-admin.co.ke/admin/
curl -s https://hodi-admin.co.ke/mobile/facilities/list/
```

Expected: `200`, `200`, and
`{"detail":"Authentication credentials were not provided."}`.

That 403 JSON is **correct** — the mobile API requires a device session.
It is not an outage.

## 3. Rollback

```bash
git log --oneline -5
git reset --hard <previous-commit>
python manage.py collectstatic --noinput
systemctl restart gunicorn
```

## IMPORTANT — `.env` on the server

`.env` is no longer tracked in git. The server's existing `.env` is
untouched by `git pull` and must stay in place. Do **not** copy the local
`.env` up: it points at the developer database.

Credentials to rotate (they were committed in 6 commits of history):
- `DB_PASS`
- `SECRET_KEY` — rotating this invalidates active sessions and password
  reset tokens, so schedule it.

## Pending hardening (NOT applied — needs verification first)

`core/settings/prod.py` lines 61-66 have these commented out:

```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

Right now `http://hodi-admin.co.ke` serves content **without redirecting to
HTTPS**, so an admin login can travel in the clear. These should be enabled.

They were deliberately left off because enabling `SECURE_SSL_REDIRECT` when
the reverse proxy does not set `X-Forwarded-Proto: https` causes an infinite
redirect loop that would take the admin site down. `SECURE_PROXY_SSL_HEADER`
is already configured, which suggests the proxy does set it — but confirm on
the server before enabling:

```bash
curl -sI https://hodi-admin.co.ke/admin/ | grep -i x-forwarded-proto
# or check the nginx/apache vhost for proxy_set_header X-Forwarded-Proto
```

Enable HSTS **last**, and start with a short `SECURE_HSTS_SECONDS` (e.g.
300) — a long max-age is cached by browsers and hard to undo.

## November 2026 upgrade: Python 3.15, Django 6.1, bulk SMS, OpenStreetMap

What changes on the server:

* **Python 3.15.2 + Django 6.1.3** in a fresh `venv`. The code still runs on
  Python 3.12+, so a plain `pip install -r requirements.txt` into the old venv
  also works; the new interpreter is the recommended step.
* **Migrations** (all additive, nothing is dropped):
  `common.0005_map_settings` (map provider columns), `sms.0001_initial`
  (SMS tables), `sms.0002_sms_permissions` (view/send/change_sms, granted to
  Super Admin and System Administrator).
* **Static files** now use `core.storage.HodiStaticFilesStorage` via
  `STORAGES` (Django 5.1 removed `STATICFILES_STORAGE`; on Django 6 the old
  setting would silently switch hashing off). `collectstatic` no longer aborts
  on the theme's missing calendar images.
* **Email** settings moved to Django 6.1's `MAILERS`; the same `EMAIL_*`
  environment variables are read, nothing to change in `.env`.

### Steps (one SSH session, from a whitelisted IP)

```bash
cd /var/www/hodi
/usr/local/bin/hodi-backup.sh                 # DB + media backup first
grep -Eq "^SECRET_KEY=.{32,}" .env && echo "SECRET_KEY ok"   # prod now refuses to start without one
git status --porcelain                        # must be empty
git rev-parse HEAD > /tmp/hodi_rollback_commit
git fetch origin main && git reset --hard origin/main

# Python 3.15 via uv (once per server)
command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh
~/.local/bin/uv python install 3.15.2
mv venv venv-py312-$(date +%Y%m%d)            # keep for rollback
~/.local/bin/uv venv --python 3.15.2 venv
~/.local/bin/uv pip install --python venv/bin/python -r requirements.txt

# SMS credentials: the Intelli-Wealth Bonga account IntelliCash already uses
grep -E '^BONGA_SMS_(CLIENT_ID|API_KEY|API_SECRET|SERVICE_ID|ENDPOINT)=' /var/www/intellicash/.env >> .env
# (or leave .env alone and enter them under Administration > SMS Settings)

export DJANGO_ENV=prod
venv/bin/python manage.py migrate --noinput
venv/bin/python manage.py collectstatic --noinput
venv/bin/python manage.py check --deploy      # expect: no issues (2 silenced)

# Background SMS sender (set User= to match hodi.service first)
cp systemd/hodi-sms.service systemd/hodi-sms.timer /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now hodi-sms.timer

systemctl restart hodi.service
```

Then run the checks in section 2, plus:

```bash
curl -s https://hodi-admin.co.ke/mobile/config/map/        # JSON with "provider"
```

In the dashboard: **SMS Settings** should say "SMS is ready to send"; send one
test SMS to your own phone. **Map Settings**: choose OpenStreetMap or Google.

### Rollback

```bash
cd /var/www/hodi
git reset --hard $(cat /tmp/hodi_rollback_commit)
rm -rf venv && mv venv-py312-YYYYMMDD venv
DJANGO_ENV=prod venv/bin/python manage.py collectstatic --noinput
systemctl disable --now hodi-sms.timer
systemctl restart hodi.service
```

The new columns and tables can stay: the old code ignores them.
