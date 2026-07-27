from users.models import ProfitRecord
from django.utils import timezone
from decimal import Decimal
from .models import ActiveInvestment
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings


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