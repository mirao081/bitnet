from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import ActiveInvestment, Notification
from users.models import ProfitRecord



def send_html_email(subject, message, user, backend_settings):
    # Render your HTML template with logo + styling
    html_content = render_to_string("users/transaction_email.html", {
        "user": user,
        "subject": subject,
        "message": message,
    })

    # Plain text fallback (no HTML tags)
    text_content = f"{subject}\n\n{message}"

    connection = get_connection(
        backend=backend_settings["EMAIL_BACKEND"],
        host=backend_settings["EMAIL_HOST"],
        port=backend_settings["EMAIL_PORT"],
        username=backend_settings["EMAIL_HOST_USER"],
        password=backend_settings["EMAIL_HOST_PASSWORD"],
        use_tls=backend_settings["EMAIL_USE_TLS"],
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # ✅ plain text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        connection=connection,
    )
    msg.attach_alternative(html_content, "text/html")  # ✅ attach HTML properly
    msg.send(fail_silently=True)



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
            fail_silently=True,
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
