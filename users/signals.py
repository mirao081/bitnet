from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Notification,
    Deposit,
    Withdrawal,
    UserKYC,
    ActiveInvestment,
    Referral,
    ReferralCommission,
    UserProfile,
    UserBalance,
    UserVerification,   # make sure this is imported
)


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
        notify(
            instance,
            "signup",
            f"Welcome {instance.username}, your account has been created!"
        )
        UserProfile.objects.get_or_create(user=instance)
        UserBalance.objects.get_or_create(user=instance)


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

        notify(
            instance.user,
            "deposit",
            f"Your deposit of {instance.amount} has been approved."
        )


@receiver(post_save, sender=Withdrawal)
def withdrawal_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        notify(
            instance.user,
            "withdrawal",
            f"Your withdrawal of {instance.amount} has been processed."
        )


@receiver(post_save, sender=UserKYC)
def kyc_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        notify(
            instance.user,
            "verification",
            f"Dear {instance.user.username}, your identity has been verified. You are now an investor with BitnetFx."
        )


@receiver(post_save, sender=ActiveInvestment)
def investment_completed(sender, instance, **kwargs):
    if instance.status == "completed":
        notify(
            instance.user,
            "investment",
            f"Your investment of {instance.amount} in {instance.plan_name} has completed its cycle. Profit has been credited to your account."
        )


@receiver(post_save, sender=Referral)
def referral_signup(sender, instance, created, **kwargs):
    if created and instance.referrer:
        notify(
            instance.referrer,
            "referral",
            f"You got a new referral: {instance.user.username} just signed up with your link!"
        )


@receiver(post_save, sender=Deposit)
def referral_bonus(sender, instance, **kwargs):
    if instance.status != "approved":
        return
    if instance.bonus_paid:
        return

    try:
        referral = Referral.objects.get(user=instance.user)
    except Referral.DoesNotExist:
        print(f"No referral record for {instance.user.username}")
        return

    if referral.referrer is None:
        print(f"{instance.user.username} has no referrer.")
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

    notify(
        referrer,
        "bonus",
        f"You earned ${bonus} (7%) from {instance.user.username}'s deposit."
    )

    print(f"{referrer.username} received ${bonus} referral bonus.")


# ✅ NEW: keep UserProfile.verification_status in sync with UserVerification.is_verified
@receiver(post_save, sender=UserVerification)
def sync_verification_status(sender, instance, **kwargs):
    try:
        profile = UserProfile.objects.get(user=instance.user)
        profile.verification_status = "verified" if instance.is_verified else "pending"
        profile.save(update_fields=["verification_status"])
    except UserProfile.DoesNotExist:
        print(f"No UserProfile found for {instance.user.username}")
