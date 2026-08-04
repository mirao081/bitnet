from django.urls import path
from . import views
from .views import contact_view

app_name = "crypto"


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('investment-plans/', views.investment_plans, name='investment_plans'),
    path('features/', views.features, name='features'),
    path('legals/', views.legals, name='legals'),
    path('affiliate/', views.affiliate, name="affiliate"),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path("twofa-verify/", views.twofa_verify, name="twofa_verify"),
    path("logout/", views.logout_view, name="logout"),
    path('teams/', views.teams, name="teams"),
    path("services/", views.services, name="services"),
    path('pages/', views.pages, name='pages'),
    path('instruments/', views.ticker_bar, name='ticker_bar'),
    path('instrument/<int:pk>/', views.instrument_detail, name='instrument_detail'),
    path("contact/", contact_view, name="contact"),
    path("faqs/", views.faqs, name="faqs"),
    path("terms/", views.terms, name="terms"),
      path("terms_detail/", views.terms_detail, name="term_detail"),
    path("faq-detail/", views.faq_detail, name="faq_detail"),
    path("terms/", views.terms, name="terms"),
    path("bitcoin-info/", views.bitcoin_info, name="bitcoin_info"),
    path("buy-bitcoin/", views.buy_bitcoin, name="buy_bitcoin"),
    path('resources/', views.resources, name='resources'),
    path('deposit-guide/', views.deposit_guide, name='deposit_guide'),
    path('market-analysis/', views.market_analysis, name='market_analysis'),
    path('bitcoin-reports/', views.bitcoin_reports, name='bitcoin_reports'),
    path('ethereum-analysis/', views.ethereum_analysis, name='ethereum_analysis'),
    path('altcoin-reports/', views.altcoin_reports, name='altcoin_reports'),
    path('crypto-glossary/', views.crypto_glossary, name='crypto_glossary'),
    path("register/", views.signup_view, name="register"),
    path("twofa-setup/", views.twofa_setup, name="twofa_setup"),
    path("twofa-reset/", views.twofa_reset, name="twofa_reset"),
    path("twofa-verify/", views.twofa_verify, name="twofa_verify"),
    path('forex-table-api/', views.forex_table_api, name='forex_table_api'),
]