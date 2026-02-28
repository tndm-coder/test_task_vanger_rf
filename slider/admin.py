from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import SliderItem


@admin.register(SliderItem)
class SliderItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("thumbnail", "title", "order")
    list_display_links = ("thumbnail", "title")
    search_fields = ("title",)
    ordering = ("order", "id")

    def thumbnail(self, obj):
        if not obj.image:
            return "—"

        try:
            image_url = obj.image.url
        except (AttributeError, ValueError, OSError):
            return "—"

        return format_html(
            '<img src="{}" alt="{}" style="height: 56px; width: 100px; object-fit: cover; border-radius: 6px;" />',
            image_url,
            obj.title,
        )

    thumbnail.short_description = "Миниатюра"
