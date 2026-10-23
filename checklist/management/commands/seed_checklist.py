from django.core.management.base import BaseCommand

from checklist.models import Item, Section

DEMO = [
    ("Pre-event setup", [
        "Confirm room layout and seating",
        "Power to all racks and check UPS status",
        "Patch and label every cable run",
        "Projector / display powered and on correct input",
    ]),
    ("Audio", [
        "Mics battery-checked and spares on hand",
        "Ring out the room and set gain structure",
        "Confirm playback from laptop and phone",
        "Record feed armed and levels verified",
    ]),
    ("Video", [
        "Camera framing and white balance set",
        "Resolution matched end to end (1080p60)",
        "Lower thirds and graphics loaded",
        "Confidence monitor visible to presenter",
    ]),
    ("Before doors open", [
        "Full dry run of the first five minutes",
        "Comms check with every operator position",
        "Backup laptop ready with the deck loaded",
        "House lights and walk-in music running",
    ]),
]


class Command(BaseCommand):
    help = "Load a starter checklist. Skips any section that already exists."

    def handle(self, *args, **options):
        for section_order, (title, items) in enumerate(DEMO, start=1):
            section, created = Section.objects.get_or_create(
                title=title, defaults={"order": section_order}
            )
            if not created:
                self.stdout.write(f"skipped (exists): {title}")
                continue
            Item.objects.bulk_create(
                Item(section=section, text=text, order=order)
                for order, text in enumerate(items, start=1)
            )
            self.stdout.write(self.style.SUCCESS(f"added: {title} ({len(items)} options)"))
