from django.db import models
from django.utils.functional import cached_property

from .markdown import render_markdown


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
    guidance = models.TextField(
        blank=True,
        help_text=(
            "How to do this option. Shown in a pop-up when the option is "
            "long-pressed. Markdown: **bold**, *italic*, [link](https://…), "
            "bullet or numbered lists, and ![caption](https://…/photo.jpg) "
            "for an image. Leave blank for no pop-up."
        ),
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text

    @cached_property
    def guidance_html(self):
        """The guidance Markdown rendered to HTML, or "" when there is none."""
        return render_markdown(self.guidance)
