from django.contrib import admin
from .models import UserVerification, UserKYC, Notification,SupportArticle,UserProfile, UserWallet
from django.core.mail import send_mail
from django.conf import settings
from .models import CompanyWallet,Referral, ReferralCommission

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
                fail_silently=False,  
            )

@admin.register(SupportArticle)
class SupportArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    search_fields = ("title", "content")
    list_filter = ("category",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "country", "timezone", "risk_level", "auto_invest")
    search_fields = ("user__username", "phone", "country")

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "btc_wallet", "eth_wallet", "usdt_erc20_wallet", "usdt_trc20_wallet")
    search_fields = ("user__username", "btc_wallet", "eth_wallet")


@admin.register(CompanyWallet)
class CompanyWalletAdmin(admin.ModelAdmin):
    list_display = ("btc_wallet", "eth_wallet", "usdt_erc20_wallet", "usdt_trc20_wallet")


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("user", "referrer", "referral_count")

    def referral_count(self, obj):
        return Referral.objects.filter(referrer=obj.user).count()

    referral_count.short_description = "Referral Count"

@admin.register(ReferralCommission)
class ReferralCommissionAdmin(admin.ModelAdmin):
    list_display = ("referrer", "referral", "deposit_amount", "commission_amount", "created_at")
    search_fields = ("referrer__username", "referral__username")
    list_filter = ("created_at",)