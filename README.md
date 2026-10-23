# avchecklist

A single-page Django checklist for AV setups, served at **av.ruansonder-r.com**.

- One public page lists every section and its tickable options.
- Ticking an option strikes it through in place — nothing is removed or reordered.
- **Clear all** unticks everything.
- Ticks are stored in the visitor's browser (`localStorage`), so they survive a
  refresh and are private to that browser. Nothing is written to the database.
- Sections and options are managed from the Django admin, which sits on an
  unguessable path (`DJANGO_ADMIN_URL`) and is not linked from the public page.
  Production uses a different path to the local default — it is set only as a
  Vercel environment variable, never committed here.

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

## Deployment

Hosted on Vercel (project `avchecklist`, region `fra1`) against a Neon Postgres
database (`avchecklist-db`) provisioned through the Vercel Marketplace, which
supplies `DATABASE_URL` automatically.

Vercel detects Django natively and serves `avchecklist/wsgi.py` itself — it also
runs `collectstatic` during the build. No `api/` entrypoint and no rewrites are
needed; a catch-all rewrite actively breaks routing, because the rewritten path
is what Django receives.

Pushing to `main` deploys to production; pull requests get preview
deployments. Migrations are **not** part of the build, so run them yourself
before pushing a change that needs them:

```bash
vercel env pull                                   # refresh .env.local
python3 scripts/manage_remote.py migrate          # migrate Neon, not local SQLite
git push                                          # deploys main to production
```

`vercel --prod` still works for deploying without a push.

`scripts/manage_remote.py` runs any manage.py command against Neon's *unpooled*
endpoint. Migrations are deliberately not part of the build — they are run
explicitly, the same way commoter does it.
