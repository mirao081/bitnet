from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("investments/", views.investments, name="investments"),
    path("investment-plans/", views.investment_plans, name="investment_plans"),
    path("wallets/", views.wallets, name="wallets"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transactions/", views.transactions, name="transactions"),
    path("profit-history/", views.profit_history, name="profit_history"),
    path("referrals/", views.referrals, name="referrals"),
    path("markets/", views.markets, name="markets"),
    path("news/", views.news, name="news"),
    path("support/", views.support, name="support"),
    path("profile/", views.profile, name="profile"),
    path("security/", views.security, name="security"),
    path("settings/", views.settings, name="settings"),
    path("ai-chat/", views.ai_chat, name="ai_chat"),  
    path('kyc-upload/', views.kyc_upload, name='kyc_upload'),
    path("deposit/", views.make_deposit, name="make_deposit"),
    path("withdrawal/", views.request_withdrawal, name="request_withdrawal"),
    path("investment/", views.start_investment, name="start_investment"),
]
