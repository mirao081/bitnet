from users.models import ProfitRecord
from django.utils import timezone
from decimal import Decimal
from .models import ActiveInvestment
from .models import Notification
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def notify(user, type, message):
    # Save notification in DB
    note = Notification.objects.create(
        user=user,
        type=type,
        message=message
    )

    # Send email if user has an email address
    if user.email:
        context = {
            "user": user,
            "subject": "New Notification from Bitnetapp",
            "message": message,
        }
        # Render HTML template
        html_content = render_to_string("users/transaction_email.html", context)

        # Create multipart email (plain text + HTML)
        email = EmailMultiAlternatives(
            subject="New Notification from Bitnetapp",
            body=message,  # plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    return note


def credit_profit(user, investment):
    profit_amount = investment.amount * (investment.roi_percent / 100)

    ProfitRecord.objects.create(
        user=user,
        investment_name=investment.plan_name,
        date=timezone.now(),
        status="Credited"
    )


def process_matured_investments():
    matured_investments = ActiveInvestment.objects.filter(
        status="active",
        end_date__lte=timezone.now()
    )
    for inv in matured_investments:
        profile = inv.user.userprofile
        roi_multiplier = Decimal("1") + (inv.roi_percent / Decimal("100"))
        payout = inv.amount * roi_multiplier

        profile.usd_balance += payout
        profile.save()

        inv.status = "completed"
        inv.save()
