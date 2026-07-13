from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification, Deposit, Withdrawal, UserKYC, ActiveInvestment, Referral
from django.core.mail import send_mail
from django.conf import settings

# Helper function
def notify(user, type, message):
    note = Notification.objects.create(
        user=user,
        type=type,
        message=message
    )
    if user.email:
        send_mail(
            subject="New Notification from BitnetFx",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    return note

# 1. User signup
@receiver(post_save, sender=User)
def new_user_notification(sender, instance, created, **kwargs):
    if created:
        notify(instance, "signup", f"Welcome {instance.username}, your account has been created!")

# 2. Deposit approved
@receiver(post_save, sender=Deposit)
def deposit_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        notify(instance.user, "deposit", f"Your deposit of {instance.amount} has been approved.")

# 3. Withdrawal approved
@receiver(post_save, sender=Withdrawal)
def withdrawal_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        notify(instance.user, "withdrawal", f"Your withdrawal of {instance.amount} has been processed.")

# 4. KYC verified
@receiver(post_save, sender=UserKYC)
def kyc_notification(sender, instance, **kwargs):
    if instance.status == "approved":
        notify(instance.user, "verification", f"Dear {instance.user.username}, your identity has been verified. You are now an investor with BitnetFx.")

# 5. Investment completed
@receiver(post_save, sender=ActiveInvestment)
def investment_completed(sender, instance, **kwargs):
    if instance.status == "completed":
        notify(instance.user, "investment", f"Your investment of {instance.amount} in {instance.plan_name} has completed its cycle. Profit has been credited to your account.")

# 6. Referral signup
@receiver(post_save, sender=Referral)
def referral_signup(sender, instance, created, **kwargs):
    if created and instance.referrer:
        notify(instance.referrer, "referral", f"You got a new referral: {instance.user.username} just signed up with your link!")

# 7. Referral bonus earned
@receiver(post_save, sender=Deposit)
def referral_bonus(sender, instance, **kwargs):
    if instance.status == "approved" and hasattr(instance.user, "referral") and instance.user.referral.referrer:
        referrer = instance.user.referral.referrer
        bonus = instance.amount * 0.05  # Example: 5% bonus
        notify(referrer, "bonus", f"You earned a referral bonus of {bonus} from {instance.user.username}'s deposit.")
