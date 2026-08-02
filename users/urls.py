from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/export/excel/", views.export_portfolio_excel, name="export_portfolio_excel"),

    path("investments/", views.investments, name="investments"),
    path("investment-plans/", views.investment_plans, name="investment_plans"),
    path("wallets/", views.wallets, name="wallets"),
    path("make-deposit/", views.make_deposit, name="make_deposit"),
  
    
    path("deposit-invoice/<int:deposit_id>/<str:currency>/", views.deposit_invoice, name="deposit_invoice"),
   
    path("withdraw/", views.withdraw, name="withdraw"),
    
    # path("management/withdrawals/", views.all_withdrawals, name="all_withdrawals"),
    # path("management/withdrawals/<int:withdrawal_id>/update/", views.update_withdrawal_status, name="update_withdrawal_status"),

  
    path("withdrawal/", views.request_withdrawal, name="request_withdrawal"),
    path("withdraw-invoice/<int:withdrawal_id>/<str:currency>/", views.withdraw_invoice, name="withdraw_invoice"),

    path("transactions/", views.transactions, name="transactions"),
    path("transactions/<int:tx_id>/receipt/", views.download_receipt, name="download_receipt"),
    path("transactions/export/csv/", views.export_transactions_csv, name="export_transactions_csv"),
    path("transactions/export/pdf/", views.export_transactions_pdf, name="export_transactions_pdf"),
    path("transactions/export/excel/", views.export_transactions_excel, name="export_transactions_excel"),


    path("profit-history/", views.profit_history, name="profit_history"),
    path("investment/<int:investment_id>/complete/", views.complete_investment, name="complete_investment"),
    path("referrals/", views.referrals, name="referrals"),
    path("markets/", views.markets, name="markets"),
    path("market-data/", views.market_data, name="market_data"),
    path("news/", views.news, name="news"),
    path("news-data/", views.news_data, name="news_data"),
    path("logout/", views.logout_view, name="logout"),
    path("support/", views.support, name="support"),
    path("profile/", views.profile, name="profile"),
    path("profile-settings/", views.profile_settings, name="profile_settings"),  
    path("quick-settings/", views.quick_settings, name="quick_settings"),  

   
    path("security-center/", views.security_center, name="security_center"),
    path("security-overview/", views.security, name="security"),         
    path("security/", views.security_center, name="security_center"),    
    path("settings/", views.settings, name="settings"),
    
    path("kyc-upload/", views.kyc_upload, name="kyc_upload"),
    path("investment/", views.start_investment, name="start_investment"),
    path("start-investment/", views.start_investment, name="start_investment"),

  
    path("security/manage-2fa/", views.manage_2fa, name="manage_2fa"),
    path("security/login-alerts/", views.login_alerts, name="login_alerts"),
    path("security/view-activity/", views.view_activity, name="view_activity"),
    path("security/revoke-sessions/", views.revoke_sessions, name="revoke_sessions"),
    path("security/verify-identity/", views.verify_identity, name="verify_identity"),
    path("security/change-password/", views.change_password, name="change_password"),
    path("security/manage-api-keys/", views.manage_api_keys, name="manage_api_keys"),
    path("security/alerts/", views.security_alerts, name="security_alerts"),

    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/export/csv/", views.export_portfolio_csv, name="export_portfolio_csv"),
    path("portfolio/export/pdf/", views.export_portfolio_pdf, name="export_portfolio_pdf"),

    path("ai-chat/", views.ai_chat, name="ai_chat"),
    path("api/recent-transactions/", views.recent_transactions_api, name="recent_transactions_api"),
    path("wallet-data/",views.wallet_data,name="wallet_data",),
    path("company-wallet/<str:asset>/",views.company_wallet,name="company_wallet",),

]
