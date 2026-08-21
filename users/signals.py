from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from .models import (
    Deposit,
    Withdrawal,
    UserKYC,
    ActiveInvestment,
    Referral,
    ReferralCommission,
    UserProfile,
    UserBalance,
    UserVerification,
    Notification,
)
from .utils import send_html_email



def notify(user, type, message):
    note = Notification.objects.create(
        user=user,
        type=type,
        message=message
    )

    if user.email and not settings.DEBUG:
        try:
            send_mail(
                subject="New Notification from BitnetFx",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            print("Email sending failed:", e)

    return note



@receiver(post_save, sender=User)
def new_user_setup(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        UserBalance.objects.get_or_create(user=instance)

        try:
            # Notify admin
            send_mail(
                subject="New User Registered",
                message=f"New user signed up: {instance.username} ({instance.email})",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["support@bitnetapp.com"],
                fail_silently=False,
            )
            # ✅ Notify user directly
            if instance.email:
                send_mail(
                    subject="Welcome to BitnetFx",
                    message=f"Dear {instance.username}, thank you for registering with BitnetFx. Your account has been created successfully.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.email],
                    fail_silently=False,
                )
        except Exception as e:
            print("Signup email failed:", e)



@receiver(user_logged_in)
def notify_admin_login(sender, request, user, **kwargs):
    print("🔔 Login signal fired for", user.username)
    send_html_email(
        subject="User Logged In",
        message=f"User {user.username} just logged in.",
        user=user,
        backend_settings=settings.SENDGRID_EMAIL_BACKEND,
    )




@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()

@receiver(post_save, sender=Deposit)
def deposit_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        profile = UserProfile.objects.get(user=instance.user)
        profile.usd_balance += instance.amount
        profile.save()

        send_html_email(
            subject="Deposit Approved",
            message=f"Your deposit of {instance.amount} has been approved and credited.",
            user=instance.user,
            backend_settings=settings.SENDGRID_EMAIL_BACKEND,
        )

@receiver(post_save, sender=Withdrawal)
def withdrawal_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        send_html_email(
            subject="Withdrawal Processed",
            message=f"Your withdrawal of {instance.amount} has been processed successfully.",
            user=instance.user,
            backend_settings=settings.SENDGRID_EMAIL_BACKEND,
        )

@receiver(post_save, sender=UserKYC)
def kyc_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        # ✅ Notify user directly
        if instance.user.email:
            send_mail(
                subject="KYC Verification Approved",
                message=f"Dear {instance.user.username}, your identity has been verified. You are now a bonafide investor with BitnetFx.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=False,
            )
        # Keep notification record
        notify(
            instance.user,
            "verification",
            f"Dear {instance.user.username}, your identity has been verified. You are now an investor with BitnetFx."
        )


@receiver(post_save, sender=ActiveInvestment)
def investment_completed(sender, instance, **kwargs):
    if instance.status == "completed":
        send_html_email(
            subject="Investment Completed",
            message=f"Your investment of {instance.amount} in {instance.plan_name} has completed. Profit credited to your account.",
            user=instance.user,
            backend_settings=settings.SENDGRID_EMAIL_BACKEND,
        )

@receiver(post_save, sender=Referral)
def referral_signup(sender, instance, created, **kwargs):
    if created and instance.referrer:
        send_html_email(
            subject="New Referral Signup",
            message=f"You got a new referral: {instance.user.username} signed up with your link!",
            user=instance.referrer,
            backend_settings=settings.SENDGRID_EMAIL_BACKEND,
        )

@receiver(post_save, sender=Deposit)
def referral_bonus(sender, instance, **kwargs):
    if instance.status != "approved" or instance.bonus_paid:
        return

    try:
        referral = Referral.objects.get(user=instance.user)
    except Referral.DoesNotExist:
        return

    if referral.referrer is None:
        return

    referrer = referral.referrer
    profile, _ = UserProfile.objects.get_or_create(user=referrer)

    bonus = instance.amount * Decimal("0.07")
    profile.bonus_balance += bonus
    profile.save()

    ReferralCommission.objects.create(
        referrer=referrer,
        referral=instance.user,
        deposit_amount=instance.amount,
        commission_amount=bonus,
    )

    instance.bonus_paid = True
    instance.save(update_fields=["bonus_paid"])

    send_html_email(
        subject="Referral Bonus Earned",
        message=f"You earned ${bonus} (7%) from {instance.user.username}'s deposit.",
        user=referrer,
        backend_settings=settings.SENDGRID_EMAIL_BACKEND,
    )

@receiver(post_save, sender=UserVerification)
def sync_verification_status(sender, instance, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=instance.user)
    new_status = "verified" if instance.is_verified else "pending"

    if profile.verification_status != new_status:
        profile.verification_status = new_status
        profile.save(update_fields=["verification_status"])
