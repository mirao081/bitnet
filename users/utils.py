from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import ActiveInvestment, Notification, ProfitRecord
from crypto.models import InvestmentPlan


def send_html_email(subject, message, user, backend_settings):
    # Render your HTML template with logo + styling
    html_content = render_to_string(
        "users/transaction_email.html",
        {
            "user": user,
            "subject": subject,
            "message": message,
        },
    )

    # Plain text fallback
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
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        connection=connection,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)


def notify(user, type, message):
    note = Notification.objects.create(
        user=user,
        type=type,
        message=message,
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
    """
    Credit one investment profit payout.

    The profit is added to the user's profit balance and recorded
    in ProfitRecord.
    """
    profit_amount = (
        investment.amount
        * (investment.roi_percent / Decimal("100"))
    ).quantize(Decimal("0.01"))

    if profit_amount <= 0:
        return Decimal("0.00")

    profile = user.userprofile

    profile.profit_balance += profit_amount
    profile.save(
        update_fields=["profit_balance"]
    )

    ProfitRecord.objects.create(
        user=user,
        investment_name=investment.plan_name,
        amount=profit_amount,
        date=timezone.now(),
        status="Credited",
    )

    return profit_amount


def process_matured_investments():
    """
    Process active investments.

    One-time plans:
        Pay one full ROI at maturity, then return the principal.

    Daily plans:
        Pay one full ROI every 24 hours for the duration of the plan,
        then return the principal on final maturity.

    The processor is idempotent because payouts_processed and
    principal_returned record what has already been completed.
    """

    now = timezone.now()

    investments = (
        ActiveInvestment.objects
        .filter(status="active")
        .select_related("user", "user__userprofile")
    )

    processed_count = 0

    for investment in investments:
        try:
            user = investment.user
            profile = user.userprofile

            # Find the original investment plan.
            plan = InvestmentPlan.objects.filter(
                name=investment.plan_name
            ).first()

            if not plan:
                continue

            # Daily plans explicitly contain "EVERY DAY".
            is_daily = "EVERY DAY" in plan.duration_text.upper()

            # Number of payout periods.
            total_payouts = max(
                1,
                plan.duration_hours // 24,
            )

            # =========================================================
            # ONE-TIME PLAN
            # =========================================================
            if not is_daily:

                if now >= investment.end_date:

                    # Pay the ROI exactly once.
                    if investment.payouts_processed == 0:
                        credit_profit(
                            user,
                            investment,
                        )

                        investment.payouts_processed = 1
                        investment.last_payout_at = now

                        investment.save(
                            update_fields=[
                                "payouts_processed",
                                "last_payout_at",
                            ]
                        )

                    # Return the original principal exactly once.
                    if not investment.principal_returned:

                        profile.investment_balance -= investment.amount

                        if profile.investment_balance < Decimal("0.00"):
                            profile.investment_balance = Decimal("0.00")

                        profile.usd_balance += investment.amount

                        profile.save(
                            update_fields=[
                                "investment_balance",
                                "usd_balance",
                            ]
                        )

                        investment.principal_returned = True
                        investment.status = "completed"

                        investment.save(
                            update_fields=[
                                "principal_returned",
                                "status",
                            ]
                        )

                    processed_count += 1

                continue

            # =========================================================
            # DAILY PLAN
            # =========================================================

            elapsed_seconds = (
                now - investment.start_date
            ).total_seconds()

            # One payout becomes due after each complete 24-hour period.
            due_payouts = int(
                elapsed_seconds // (24 * 60 * 60)
            )

            # Never process more payouts than the plan allows.
            due_payouts = min(
                due_payouts,
                total_payouts,
            )

            # Catch up missed daily payouts.
            while (
                investment.payouts_processed
                < due_payouts
            ):
                credit_profit(
                    user,
                    investment,
                )

                investment.payouts_processed += 1

                investment.last_payout_at = (
                    investment.start_date
                    + timedelta(
                        days=investment.payouts_processed
                    )
                )

                investment.save(
                    update_fields=[
                        "payouts_processed",
                        "last_payout_at",
                    ]
                )

                processed_count += 1

            # =========================================================
            # FINAL MATURITY
            # =========================================================

            if (
                now >= investment.end_date
                and investment.payouts_processed >= total_payouts
                and not investment.principal_returned
            ):

                # Remove the principal from the investment balance.
                profile.investment_balance -= investment.amount

                if profile.investment_balance < Decimal("0.00"):
                    profile.investment_balance = Decimal("0.00")

                # Return the original principal to USD balance.
                profile.usd_balance += investment.amount

                profile.save(
                    update_fields=[
                        "investment_balance",
                        "usd_balance",
                    ]
                )

                investment.principal_returned = True
                investment.status = "completed"

                investment.save(
                    update_fields=[
                        "principal_returned",
                        "status",
                    ]
                )

        except Exception:
            # One problematic investment must not stop the processor
            # from processing other users' investments.
            continue

    return processed_count


def format_currency(amount):
    """
    Format a numeric amount as USD currency with a dollar sign,
    commas for thousands, and two decimal places.
    """
    try:
        return "${:,.2f}".format(float(amount))
    except Exception:
        return f"${amount}"