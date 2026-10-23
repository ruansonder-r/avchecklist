from django.contrib import admin

from .models import Item, Section


class ItemInline(admin.TabularInline):
    model = Item
    extra = 3
    fields = ["order", "text"]
    ordering = ["order", "id"]


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
    list_display = ["text", "section", "order"]
    list_editable = ["order"]
    list_filter = ["section"]
    search_fields = ["text"]
