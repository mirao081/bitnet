from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import (
    SiteSetting, NavigationLink, PageContent,
    AccessibleSection, AccessibleCard,
    InvestmentPlanSlide, InvestmentPlanCard, InvestmentPlan,
    AboutUs, TokenSaleSection, SwingSection, ExchangeSection,
    BitcoinCalculator, FeatureItem,MarketInstrument,
)
from .forms import ContactForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import logout
from users.models import UserBalance, Referral
from django.contrib.auth.models import User



def home(request):
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
    
    return render(request, "home.html", {
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
      
    })

def about(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="about").first()
    about = AboutUs.objects.first()

    return render(request, "about.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
        "about": about,
    })

def investment_plans(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="investment-plans").first()
    slides = InvestmentPlanSlide.objects.order_by("order")
    cards = InvestmentPlanCard.objects.order_by("order")
    about = AboutUs.objects.first()
    plans = InvestmentPlan.objects.all()
    return render(request, "investment_plans.html", {
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
    return render(request, "legals.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def pages(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="pages").first()
    return render(request, "pages.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def affiliate(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="affiliate").first()

    return render(request, "affiliate.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })
def teams(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="teams").first()
    return render(request, "teams.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def signup_view(request, referral_code=None):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()

        # Create default balance and referral record
        UserBalance.objects.create(user=user, balance=0.00)
        Referral.objects.create(user=user, count=0)

        # If referral code was passed
        if referral_code:
            try:
                referrer = User.objects.get(username=referral_code)
                referral, created = Referral.objects.get_or_create(user=referrer)
                referral.count += 1
                referral.save()
            except User.DoesNotExist:
                pass

        return redirect('login')
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('users:dashboard')   
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def services(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="services").first()
    return render(request, "services.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def features(request):
    settings = SiteSetting.objects.first()
    nav_links = NavigationLink.objects.all()
    page = PageContent.objects.filter(slug="features").first()
    return render(request, "features.html", {
        "settings": settings,
        "nav_links": nav_links,
        "page": page,
    })

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save or send message to support (to be built later)
            # Example: save to database or send email
            pass
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})

def faqs(request):
    return render(request, "faqs.html")

def faq_detail(request):
    return render(request, "faqs-content.html")

def terms(request):
    return render(request, "terms.html")

def terms_detail(request):
    return render(request, "terms_content.html")

def bitcoin_info(request):
    return render(request, "bitcoin_info.html")

def buy_bitcoin(request):
    return render(request, "buy_bitcoin.html")

def resources(request):
    return render(request, 'resources.html')

def deposit_guide(request):
    return render(request, 'deposit_guide.html')

def market_analysis(request):
    return render(request, 'market_analysis.html')

def bitcoin_reports(request):
    return render(request, 'bitcoin_reports.html')

def ethereum_analysis(request):
    return render(request, 'ethereum_analysis.html')

def altcoin_reports(request):
    return render(request, 'altcoin_reports.html')

def crypto_glossary(request):
    return render(request, 'crypto_glossary.html')


def ticker_bar(request):
    instruments = MarketInstrument.objects.all()
    return render(request, 'base.html', {'instruments': instruments})

def instrument_detail(request, pk):
    instrument = get_object_or_404(MarketInstrument, pk=pk)
    return render(request, 'instrument_detail.html', {'instrument': instrument})

