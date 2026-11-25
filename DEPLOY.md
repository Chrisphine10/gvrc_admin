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

**Done on 25 Nov 2026** (c3629d2 -> branch `upgrade/django-6-sms-osm`), rehearsed
first on a copy of the production database. How the server is laid out now:

* **Settings:** `.env` has `DJANGO_ENV=prod` (production used to run
  `core.settings.dev`), plus `SITE_URL`, `ENABLE_SMS_NETWORK_CALLS=true` and the
  `BONGA_SMS_*` values. `core/settings/__init__.py` reads `DJANGO_ENV` from
  `.env`, so `manage.py` agrees with the web workers. The drop-in
  `/etc/systemd/system/hodi.service.d/upgrade.conf` also sets `DJANGO_ENV=prod`
  and `GUNICORN_CMD_ARGS=--no-control-socket`: gunicorn 27 otherwise tries to
  create `/var/www/.gunicorn`, which www-data cannot write.
* **Python:** 3.15.2 from uv (`/opt/uv/bin/uv`, interpreters in `/opt/python`,
  readable by www-data). `venv` is a symlink to `venv-py315`; the old 3.12 venv
  is `venv-py312-old`. To run with the old one: `venv-py312-old/bin/python -m gunicorn ...`.
* **Bonga credentials** came from IntelliCash, which keeps them **encrypted in
  its database** (`IntegrationConfig`, provider `BONGA_SMS`), not in a `.env`.
  They were decrypted with IntelliCash's own code via
  `apps/api/prisma/run-with-service-env.sh` into a root-only file and appended
  to Hodi's `.env`; nothing was printed.
* **SMS timer:** `hodi-sms.timer` runs `send_sms_broadcasts` every minute.
* **Mail:** `.env` has no `EMAIL_HOST`, so prod uses the dummy mail backend
  (mail is discarded, never printed into the log) and `mail.E001` is silenced.
  Password reset links go by SMS. Set the `EMAIL_*` values to turn email on.
* **Ownership:** the tree is www-data, but `.git` must stay **root**-owned, or
  root's git refuses it ("dubious ownership"). After `chown -R www-data`, run
  `chown -R root:root /var/www/hodi/.git`.
* `staticfiles/` is tracked in git, so `git status` shows it modified after
  every `collectstatic`. That is expected.
* **Logs:** `logs/django.log` rotates at 10 MB x 5. The old 300 MB logs were
  gzipped.
* **Backups taken:** `/var/backups/hodi/<timestamp>*/` (database, `.env`, old commit).

### Routine update (one SSH session, from a whitelisted IP)

The server's checked-out branch cannot be pushed to, so push to a side ref:

```bash
# on your PC
git push vps:/var/www/hodi upgrade/django-6-sms-osm:refs/heads/incoming
```

```bash
# on the server
cd /var/www/hodi
B=/var/backups/hodi/$(date -u +%Y%m%d%H%M%S); mkdir -p $B; git rev-parse HEAD > $B/commit
python3 -c "import sqlite3;s=sqlite3.connect('file:db.sqlite3?mode=ro',uri=True);d=sqlite3.connect('$B/db.sqlite3');s.backup(d)"
git merge --ff-only incoming && git branch -D incoming
chown -R www-data:www-data . && chown -R root:root .git
M="sudo -u www-data venv/bin/python manage.py"
$M migrate --noinput && $M collectstatic --noinput -v0 && $M check --deploy
systemctl restart hodi
curl -s -o /dev/null -w '%{http_code}
' --resolve hodi-admin.co.ke:443:127.0.0.1 https://hodi-admin.co.ke/login/   # 200
$M check_data          # read-only data report; expect 0 errors
```

Rollback: `git reset --hard $(cat $B/commit)`, put `$B/db.sqlite3` back if a
migration ran, fix ownership as above, `systemctl restart hodi`.

The GitHub "Deploy to production" workflow still cannot reach the server (its
SSH is blocked since the November hardening), so merging into `main` changes
nothing on the server; deploy by hand as above.
