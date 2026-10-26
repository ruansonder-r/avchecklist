from textwrap import dedent

from django.core.management.base import BaseCommand

from checklist.models import Item, Section

# An option is either plain text, or (text, guidance) where the guidance is the
# Markdown shown when the option is long-pressed on the checklist.
#
# Keep each step on a single source line: a newline in guidance is rendered as
# a line break, so wrapping a sentence here would wrap it in the pop-up too.
DEMO = [
    ("Pre-event setup", [
        "Confirm room layout and seating",
        ("Power to all racks and check UPS status", """
            1. Bring racks up **one at a time** — amps last, always.
            2. On each UPS, check the load is under 70% and the battery indicator is solid, not flashing.
            3. Note the runtime estimate. Under 8 minutes means the batteries are due for replacement — flag it, don't ignore it.

            > If a UPS beeps on self-test, swap it out now rather than discovering it mid-show.
        """),
        ("Patch and label every cable run", """
            Label **both ends** of every run before it leaves the rack.

            - Source, destination and signal type, e.g. `FOH-3 → Stage L / XLR`
            - Tape goes on the connector body, not the cable jacket
            - Spare runs get labelled too, so a swap takes seconds

            Walk the room afterwards and tug-test anything crossing a doorway or walkway.
        """),
        "Projector / display powered and on correct input",
    ]),
    ("Audio", [
        "Mics battery-checked and spares on hand",
        ("Ring out the room and set gain structure", """
            1. Start with all channel gains down and the master at unity.
            2. Bring one mic up until it just rings, then pull it back 6 dB.
            3. Notch the ringing frequency — narrow Q, no more than 3 dB of cut.
            4. Repeat for each ringing frequency, up to about four of them.

            Aim for peaks around **-18 dBFS** on the meters. If you are running out of headroom at the master, the gain structure is wrong further upstream.
        """),
        "Confirm playback from laptop and phone",
        ("Record feed armed and levels verified", """
            Check all three before you call it armed:

            - The recorder shows **armed**, not just powered
            - Levels are moving on the meters during a real sound check
            - There is room for the full session plus an hour

            Then record 30 seconds and play it back. An armed recorder with no input sounds exactly like a working one until you need it.
        """),
    ]),
    ("Video", [
        ("Camera framing and white balance set", """
            1. Frame with the presenter's eyes on the upper third line.
            2. Leave a little headroom — not a lot.
            3. White balance off a white card **under the show lighting**, not the house lights.

            Re-check white balance if the lighting state changes between rehearsal and doors.
        """),
        "Resolution matched end to end (1080p60)",
        "Lower thirds and graphics loaded",
        "Confidence monitor visible to presenter",
    ]),
    ("Before doors open", [
        ("Full dry run of the first five minutes", """
            Run it as if it were live: walk-in music down, lights to show state, first slide up, presenter mic open.

            The first five minutes is where almost every failure shows up — wrong input, dead battery, unmuted channel, missing cue.
        """),
        "Comms check with every operator position",
        "Backup laptop ready with the deck loaded",
        "House lights and walk-in music running",
    ]),
]


def split(option):
    """Normalise an option into (text, guidance)."""
    if isinstance(option, tuple):
        text, guidance = option
        return text, dedent(guidance).strip()
    return option, ""


class Command(BaseCommand):
    help = "Load a starter checklist. Skips any section that already exists."

    def handle(self, *args, **options):
        for section_order, (title, options) in enumerate(DEMO, start=1):
            section, created = Section.objects.get_or_create(
                title=title, defaults={"order": section_order}
            )
            if not created:
                self.stdout.write(f"skipped (exists): {title}")
                continue
            Item.objects.bulk_create(
                Item(section=section, text=text, guidance=guidance, order=order)
                for order, (text, guidance) in enumerate(
                    (split(option) for option in options), start=1
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"added: {title} ({len(options)} options)")
            )
