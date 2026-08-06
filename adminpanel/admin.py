from django.contrib import admin
from users.models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "verification_status", "country", "phone")
    list_filter = ("verification_status", "country")
    search_fields = ("user__username", "phone")
