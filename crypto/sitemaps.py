from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "crypto:home",
            "crypto:about",
            "crypto:faqs",
            "crypto:terms",
            "crypto:contact",
            "crypto:bitcoin_info",
            "crypto:buy_bitcoin",
            "crypto:bitcoin_reports",
            "crypto:signup",
            "crypto:login",
        ]

    def location(self, item):
        return reverse(item)