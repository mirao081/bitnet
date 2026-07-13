from .models import SiteSetting, MarketInstrument, NavigationLink

def ticker_instruments(request):
    return {
        "instruments": MarketInstrument.objects.all()
    }

def global_settings(request):
    return {
        "settings": SiteSetting.objects.first(),
        "nav_links": NavigationLink.objects.filter(parent__isnull=True).prefetch_related("children"),
    }
