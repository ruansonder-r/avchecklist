import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create or reset the admin user from DJANGO_SUPERUSER_USERNAME / "
        "_PASSWORD / _EMAIL. Does nothing if those are not set."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME/_PASSWORD not set — skipping.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"{'created' if created else 'updated'} superuser {username}")
        )
