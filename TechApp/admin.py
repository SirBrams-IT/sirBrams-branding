from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, PortfolioItem

admin.site.site_header = "SirBrams Admin"
admin.site.site_title = "SirBrams Admin"
admin.site.index_title = "Manage your website"


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'short_message', 'is_replied', 'created_at')
    list_filter = ('is_replied',)
    search_fields = ('name', 'email', 'subject')
    actions = ['mark_as_replied']

    @admin.display(description="Message")
    def short_message(self, obj):
        text = obj.message or ""
        return text if len(text) <= 80 else text[:77] + "..."

    @admin.action(description="Mark selected messages as replied")
    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True)
        self.message_user(request, "Selected messages marked as replied.")


admin.site.register(Contact, ContactAdmin)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    """Add, edit, reorder and hide portfolio work without touching code."""

    list_display = ('thumb', 'title', 'category', 'tag', 'is_published', 'order', 'created_at')
    list_display_links = ('thumb', 'title')
    list_editable = ('is_published', 'order')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'tag', 'summary')
    readonly_fields = ('preview', 'created_at', 'updated_at')
    actions = ['publish', 'unpublish']

    fieldsets = (
        ("What is it?", {
            'fields': ('category', 'title', 'tag', 'summary'),
        }),
        ("Image", {
            'fields': ('image', 'preview'),
        }),
        ("Websites and systems only", {
            'fields': ('stack', 'url'),
            'description': "Leave these empty for graphic design.",
        }),
        ("Graphic design only", {
            'fields': ('notes',),
            'description': "Shown in the large preview next to the design.",
        }),
        ("Visibility", {
            'fields': ('is_published', 'order', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description="Image")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" alt="" style="width:64px;height:44px;object-fit:cover;border-radius:4px;">',
                obj.image.url,
            )
        return "-"

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" alt="" style="max-width:320px;max-height:240px;border-radius:6px;border:1px solid #ddd;">',
                obj.image.url,
            )
        return "Upload an image above and save to see a preview."

    @admin.action(description="Show selected items on the website")
    def publish(self, request, queryset):
        n = queryset.update(is_published=True)
        self.message_user(request, f"{n} item(s) are now visible.")

    @admin.action(description="Hide selected items from the website")
    def unpublish(self, request, queryset):
        n = queryset.update(is_published=False)
        self.message_user(request, f"{n} item(s) hidden.")
