from django.db import models


class Section(models.Model):
    """A heading on the checklist, e.g. "Before take-off"."""

    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Item(models.Model):
    """A single tickable option underneath a section."""

    section = models.ForeignKey(
        Section, related_name="items", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text
