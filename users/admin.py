from django.contrib import admin
from .models import UserVerification, UserKYC, Notification
from django.core.mail import send_mail
from django.conf import settings

@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__username',)

@admin.register(UserKYC)
class UserKYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "message", "timestamp", "is_read")
    list_filter = ("type", "is_read")
    search_fields = ("user__username", "message")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.user.email:
            send_mail(
                subject="New Notification from BitnetFx",
                message=obj.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.user.email],
                fail_silently=False,  # show errors during testing
            )
