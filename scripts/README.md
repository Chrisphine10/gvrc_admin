# scripts/

One-off and maintenance tools. Run them from the project root so Django finds
`manage.py`'s settings, e.g. `venv/bin/python scripts/verify_relationships.py`.
They are not part of the web app and pytest does not collect them
(`testpaths` in pytest.ini).

Regular checks live in management commands instead:

* `python manage.py check_data` - read-only data consistency report
* `python manage.py send_sms_broadcasts` - finish queued bulk SMS (run by `hodi-sms.timer`)
