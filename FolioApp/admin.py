from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','phone', 'email', 'subject', 'message', 'is_replied', 'created_at')
    list_filter = ('is_replied',)
    search_fields = ('name', 'email', 'subject')
    actions = ['mark_as_replied']

    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True)
        self.message_user(request, "Selected messages marked as replied.")
    mark_as_replied.short_description = "Mark selected messages as replied"

admin.site.register(Contact, ContactAdmin)
