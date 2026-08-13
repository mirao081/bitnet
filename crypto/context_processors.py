from .models import SiteSetting, MarketInstrument, NavigationLink
from django.conf import settings

def ticker_instruments(request):
    return {
        "instruments": MarketInstrument.objects.all()
    }

def global_settings(request):
    return {
        "settings": SiteSetting.objects.first(),
        "nav_links": NavigationLink.objects.filter(parent__isnull=True).prefetch_related("children"),
    }

def recaptcha_key(request):
    return {
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY
    }
