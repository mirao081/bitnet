from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from .models import (
    SiteSetting, NavigationLink, PageContent,
    AccessibleSection, AccessibleCard,
    InvestmentPlanSlide, InvestmentPlanCard, InvestmentPlan,
    AboutUs, TokenSaleSection, SwingSection, ExchangeSection,
    BitcoinCalculator, FeatureItem, MarketInstrument
)
from .forms import ContactForm, StyledSignupForm
from users.models import (
    ActiveInvestment, UserBalance, Referral,
    UserVerification, SecurityAlert, LoginHistory,UserProfile
)
import pyotp
import base64
import qrcode
import qrcode.image.svg
import user_agents


User = get_user_model()

# def home(request):
#     # Save referral code in session
#     referral_code = request.GET.get("ref")
#     if referral_code:
#         request.session["referral_code"] = referral_code

#     settings = SiteSetting.objects.first()
#     nav_links = NavigationLink.objects.all()
#     page = PageContent.objects.filter(slug="home").first()
#     accessible = AccessibleSection.objects.first()
#     accessible_cards = AccessibleCard.objects.order_by("order")[:5]
#     token_sale = TokenSaleSection.objects.first()
#     swing_section = SwingSection.objects.first()
#     exchange_section = ExchangeSection.objects.first()
#     plans = InvestmentPlan.objects.all()
#     calculator = BitcoinCalculator.objects.first()
#     feature_items = FeatureItem.objects.all()
#     instruments = MarketInstrument.objects.all()

#     return render(request, "crypto/home.html", {
#         "settings": settings,
#         "nav_links": nav_links,
#         "page": page,
#         "accessible": accessible,
#         "accessible_cards": accessible_cards,
#         "token_sale": token_sale,
#         "swing_section": swing_section,
#         "exchange_section": exchange_section,
#         "plans": plans,
#         "calculator": calculator,
#         "feature_items": feature_items,
#         "instruments": instruments,
#     })


def home(request):
    referral_code = request.GET.get("ref")

    if referral_code:
        request.session["referral_code"] = referral_code
        print(f"Referral saved in session: {referral_code}")

    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="home").first()
    accessible = AccessibleSection.objects.first()
    accessible_cards = AccessibleCard.objects.order_by("order")[:5]
    token_sale = TokenSaleSection.objects.first()
    swing_section = SwingSection.objects.first()
    exchange_section = ExchangeSection.objects.first()
    plans = InvestmentPlan.objects.all()
    calculator = BitcoinCalculator.objects.first()
    feature_items = FeatureItem.objects.all()
    instruments = MarketInstrument.objects.all()

    context = {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
        "accessible": accessible,
        "accessible_cards": accessible_cards,
        "token_sale": token_sale,
        "swing_section": swing_section,
        "exchange_section": exchange_section,
        "plans": plans,
        "calculator": calculator,
        "feature_items": feature_items,
        "instruments": instruments,
    }

    return render(request, "crypto/home.html", context)


def about(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="about").first()
    about = AboutUs.objects.first()

    return render(request, "crypto/about.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
        "about": about,
    })

@login_required
def investment_plans(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="investment-plans").first()
    slides = InvestmentPlanSlide.objects.order_by("order")
    cards = InvestmentPlanCard.objects.order_by("order")
    about = AboutUs.objects.first()
    plans = InvestmentPlan.objects.all()

    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        amount = request.POST.get("amount")
        plan = InvestmentPlan.objects.get(id=plan_id)
        end_date = timezone.now() + timedelta(hours=plan.duration_hours)

        ActiveInvestment.objects.create(
            user=request.user,
            plan_name=plan.name,
            amount=amount,
            start_date=timezone.now(),
            end_date=end_date,
            status="active"
        )

        messages.success(
            request,
            f"You have successfully invested in {plan.name}. "
            f"Maturity will be on {end_date.strftime('%Y-%m-%d %H:%M:%S')}."
        )
        return redirect("users:investment_plans")

    return render(request, "crypto/investment_plans.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
        "slides": slides,
        "cards": cards,
        "about": about,
        "plans": plans,
    })

def legals(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="teams").first()
    return render(request, "crypto/legals.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def pages(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="pages").first()
    return render(request, "crypto/pages.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def affiliate(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="affiliate").first()

    return render(request, "crypto/affiliate.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def teams(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="teams").first()
    return render(request, "crypto/teams.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            verification, _ = UserVerification.objects.get_or_create(user=user)
            login(request, user)
            ua_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = user_agents.parse(ua_string)
            device = f"{user_agent.browser.family} ({user_agent.os.family})"
            ip = get_client_ip(request)

            LoginHistory.objects.create(
                user=user,
                timestamp=timezone.now(),
                ip=ip,
                device=device,
                status="Successful"
            )
            if user.is_staff or user.is_superuser:
                return redirect("adminpanel:dashboard")
            return redirect("users:dashboard")

        else:
            ip = get_client_ip(request)
            username = request.POST.get("username")
            user = User.objects.filter(username=username).first()

            if user:
                SecurityAlert.objects.create(
                    user=user,
                    event=f"Failed login attempt from IP {ip}",
                    status="Blocked"
                )

            messages.error(request, "Invalid credentials.")

    return render(request, "crypto/login.html", {"form": form})


def twofa_verify(request):
    if request.method == "POST":
        code = request.POST.get("otp")
        user_id = request.session.get("pre_2fa_user_id")
        if user_id:
            User = get_user_model()
            user = User.objects.get(id=user_id)
        else:
            user = request.user

        try:
            verification = UserVerification.objects.get(user=user)
        except UserVerification.DoesNotExist:
            messages.error(request, "2FA not set up. Please configure first.")
            return redirect("crypto:login")

        if not verification.secret:
            messages.error(request, "2FA not set up. Please configure first.")
            return redirect("crypto:login")

        totp = pyotp.TOTP(verification.secret)
        print("Server expects:", totp.now())

        if totp.verify(code, valid_window=1):  
            login(request, user)
            if "pre_2fa_user_id" in request.session:
                del request.session["pre_2fa_user_id"]
            verification.is_verified = True
            verification.save()
            messages.success(request, "Login successful with 2FA.")
            return redirect("users:dashboard")
        else:
            messages.error(request, "Invalid 2FA code. Please try again.")

    return render(request, "users/twofa_verify.html")


    
def twofa_setup(request):
    user = request.user
    verification, _ = UserVerification.objects.get_or_create(user=user)

    if not verification.secret:
        verification.secret = pyotp.random_base32()
        verification.save()

    totp = pyotp.TOTP(verification.secret)
    uri = totp.provisioning_uri(name=user.email, issuer_name="BitnetFx")
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "users/twofa_setup.html", {"qr_code": qr_base64})

def twofa_reset(request):
    user = request.user
    verification, _ = UserVerification.objects.get_or_create(user=user)

    verification.secret = pyotp.random_base32()
    verification.is_verified = False
    verification.save()

    messages.info(request, "Your 2FA has been reset. Please scan the new QR code.")
    return redirect("crypto:twofa_setup")


def logout_view(request):
    logout(request)
    return redirect('users:login')


def services(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="services").first()
    return render(request, "crypto/services.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def features(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="features").first()
    return render(request, "crypto/features.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the submitted information
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            service = form.cleaned_data["service"]
            message = form.cleaned_data["message"]

            # For now, simply process the form successfully
            # You can add email sending later.
            return redirect("crypto:contact")
    else:
        form = ContactForm()

    return render(request, "crypto/contact.html", {"form": form})

def signup_view(request):
    form = StyledSignupForm(request.POST or None)

    ref = request.GET.get("ref")
    if ref:
        request.session["referral_code"] = ref

    if request.method == "POST":
        if form.is_valid():
            # Save the User
            user = form.save()

            # ✅ Create a UserProfile automatically
            UserProfile.objects.get_or_create(user=user)

            # Handle referral logic
            new_referral, created = Referral.objects.get_or_create(user=user)
            referral_code = request.session.get("referral_code")

            if referral_code:
                try:
                    referrer = User.objects.get(username__iexact=referral_code)

                    if referrer != user:
                        new_referral.referrer = referrer
                        new_referral.save()

                        user.userprofile.referrer = referrer
                        user.userprofile.save()

                        print(f"{user.username} was referred by {referrer.username}")

                    request.session.pop("referral_code", None)

                except User.DoesNotExist:
                    print(f"Invalid referral code: {referral_code}")

            messages.success(
                request,
                "Your account has been created successfully. Please log in."
            )
            return redirect("crypto:login")

        else:
            print("=" * 50)
            print(form.errors.as_json())
            print("=" * 50)
            messages.error(
                request,
                "Please correct the errors below."
            )

    return render(
        request,
        "crypto/signup.html",
        {"form": form}
    )

def faqs(request):
    return render(request, "crypto/faqs.html")

def faq_detail(request):
    return render(request, "crypto/faqs-content.html")

def terms(request):
    return render(request, "crypto/terms.html")

def terms_detail(request):
    return render(request, "terms_content.html")

def bitcoin_info(request):
    return render(request, "crypto/bitcoin_info.html")

def buy_bitcoin(request):
    return render(request, "crypto/buy_bitcoin.html")

def resources(request):
    return render(request, 'crypto/resources.html')

def deposit_guide(request):
    return render(request, 'crypto/deposit_guide.html')

def market_analysis(request):
    return render(request, 'crypto/market_analysis.html')

def bitcoin_reports(request):
    return render(request, 'crypto/bitcoin_reports.html')

def ethereum_analysis(request):
    return render(request, 'crypto/ethereum_analysis.html')

def altcoin_reports(request):
    return render(request, 'crypto/altcoin_reports.html')

def crypto_glossary(request):
    return render(request, 'crypto/crypto_glossary.html')


def ticker_bar(request):
    instruments = MarketInstrument.objects.all()
    return render(request, 'crypto_base.html', {'instruments': instruments})

def instrument_detail(request, pk):
    instrument = get_object_or_404(MarketInstrument, pk=pk)
    return render(request, 'crypto:instrument_detail.html', {'instrument': instrument})

def forex_table_api(request):
    data = {"message": "Forex API placeholder"}
    return JsonResponse(data)