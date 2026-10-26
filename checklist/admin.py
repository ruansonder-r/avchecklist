from django import forms
from django.contrib import admin
from django.db import models

from .models import Item, Section

# Guidance is usually a few short steps, so give it a textarea that fits the
# inline row instead of Django's full-height default.
COMPACT_TEXTAREA = {
    models.TextField: {"widget": forms.Textarea(attrs={"rows": 4, "cols": 50})}
}


class ItemInline(admin.TabularInline):
    model = Item
    extra = 3
    fields = ["order", "text", "guidance"]
    ordering = ["order", "id"]
    formfield_overrides = COMPACT_TEXTAREA


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "item_count"]
    list_editable = ["order"]
    search_fields = ["title"]
    inlines = [ItemInline]

    @admin.display(description="Options")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["text", "section", "order", "has_guidance"]
    list_editable = ["order"]
    list_filter = ["section"]
    search_fields = ["text", "guidance"]

    @admin.display(description="Guidance", boolean=True)
    def has_guidance(self, obj):
        return bool(obj.guidance.strip())
