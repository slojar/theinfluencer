from django.contrib import admin
from .models import Page, Profile


class PageTabularInlineAdmin(admin.TabularInline):
    model = Page
    exclude = []


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role_type', 'created_on', 'updated_on']
    list_filter = ['gender', 'created_on', 'updated_on', 'role_type', 'location']
    inlines = [PageTabularInlineAdmin]


admin.site.register(Profile, ProfileAdmin)

