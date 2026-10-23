#!/usr/bin/env python3
"""Run a manage.py command against the Neon database instead of local SQLite.

Reads DATABASE_URL_UNPOOLED out of .env.local (written by `vercel env pull`)
and hands it to manage.py as DATABASE_URL. The unpooled endpoint is used
because migrations are DDL and should not go through PgBouncer.

    python3 scripts/manage_remote.py migrate
    python3 scripts/manage_remote.py seed_checklist
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env.local"
PYTHON = ROOT / ".venv" / "bin" / "python"


def load_url():
    if not ENV_FILE.exists():
        sys.exit(f"{ENV_FILE} not found — run `vercel env pull` first.")
    for line in ENV_FILE.read_text().splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == "DATABASE_URL_UNPOOLED":
            return value.strip().strip('"').strip("'")
    sys.exit("DATABASE_URL_UNPOOLED not found in .env.local.")


if len(sys.argv) < 2:
    sys.exit(__doc__)

env = {**os.environ, "DATABASE_URL": load_url()}
sys.exit(subprocess.run([str(PYTHON), str(ROOT / "manage.py"), *sys.argv[1:]], env=env).returncode)
