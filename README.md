# avchecklist

A single-page Django checklist for AV setups, served at **av.ruansonder-r.com**.

- One public page lists every section and its tickable options.
- Ticking an option strikes it through in place — nothing is removed or reordered.
- **Clear all** unticks everything.
- Ticks are stored in the visitor's browser (`localStorage`), so they survive a
  refresh and are private to that browser. Nothing is written to the database.
- Sections and options are managed from the Django admin, which sits on an
  unguessable path (`DJANGO_ADMIN_URL`) and is not linked from the public page.

## Local development

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_checklist     # optional starter content
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

- Checklist: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/console-8f21c4b2/

## Environment variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key | insecure dev key |
| `DJANGO_DEBUG` | `true` / `false` | `true` |
| `DJANGO_ADMIN_URL` | Path the admin is mounted on | `console-8f21c4b2/` |
| `DATABASE_URL` | Postgres URL in production | local SQLite file |
