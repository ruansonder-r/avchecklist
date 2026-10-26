# avchecklist

A single-page Django checklist for AV setups, served at **av.ruansonder-r.com**.

- One public page lists every section and its tickable options.
- Ticking an option strikes it through in place — nothing is removed or reordered.
- **Clear all** unticks everything.
- An option can carry *guidance* — how to actually do it. Options that have it
  show a small ⓘ badge; **long-pressing** the option (or tapping the badge, or
  right-clicking on a desktop) opens it in a pop-up. The long press is held for
  450 ms, shows a fill bar while it is held, and deliberately does **not** tick
  the option on the way out.
- Guidance is written as Markdown in the admin — bold, lists, links, tables,
  code. Images embed by URL, `![caption](https://…/photo.jpg)`; there is no
  upload, because Vercel's filesystem is read-only, so the image has to be
  hosted somewhere already.
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

## Guidance pop-ups

`Item.guidance` holds Markdown, rendered to HTML server-side by
`checklist/markdown.py` and parked in an inert `<template>` next to the option
— there is no fetch when the pop-up opens. Guidance is authored only by a
logged-in superuser in the admin, so raw HTML is deliberately left to pass
through; that is what makes an `<img>` or an embed possible at all.

A single newline is rendered as a line break, so write each step on one line
and let it wrap. A list may start on the line straight after a sentence, which
plain Markdown would not allow.

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

The guidance field is one such change — `checklist/migrations/0002_item_guidance.py`
has to reach Neon before the deploy that uses it.

`vercel --prod` still works for deploying without a push.

`scripts/manage_remote.py` runs any manage.py command against Neon's *unpooled*
endpoint. Migrations are deliberately not part of the build — they are run
explicitly, the same way commoter does it.
