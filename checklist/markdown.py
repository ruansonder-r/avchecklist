"""Rendering for the Markdown an admin writes into an item's guidance.

Guidance is only ever authored through the Django admin by a logged-in
superuser, so raw HTML is deliberately left to pass through — it is what lets
an admin drop in an <img> or an embed that Markdown cannot express. None of
this is reachable by an untrusted visitor.
"""

import re

import markdown
from django.utils.safestring import mark_safe

# One parser, reused — building a Markdown instance is the expensive part.
# `extra` brings tables, fenced code and footnotes; `nl2br` makes a single
# newline a line break, which is how a textarea reads to anyone not thinking
# in Markdown.
_renderer = markdown.Markdown(extensions=["extra", "nl2br"])

_LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])\s+\S")


def _loosen_lists(text):
    """Let a list start on the line straight after a sentence.

    Python-Markdown needs a blank line before a list, so the very natural

        Do this:
        - step one

    otherwise renders as one run-on paragraph. Insert the blank line for the
    author. Lines already inside a list are left alone, so a tight list stays
    tight rather than sprouting <p> tags inside every <li>.
    """
    out = []
    in_list = False
    for line in text.split("\n"):
        if _LIST_ITEM.match(line):
            if not in_list and out and out[-1].strip():
                out.append("")
            in_list = True
        elif line.strip() and not line[:1].isspace():
            in_list = False
        out.append(line)
    return "\n".join(out)


def render_markdown(text):
    """Render guidance Markdown to HTML. Blank input renders as ""."""
    if not text or not text.strip():
        return ""
    _renderer.reset()
    return mark_safe(_renderer.convert(_loosen_lists(text)))
