# users/utils.py
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings

def notify(user, type, message):
    # Save notification in database
    note = Notification.objects.create(
        user=user,
        type=type,
        message=message
    )

    # Send email if user has email
    if user.email:
        send_mail(
            subject="New Notification from BitnetFx",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    return note
