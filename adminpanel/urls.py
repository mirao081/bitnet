from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="dashboard"),
    path("investment-plans/", views.admin_investment_plans, name="admin_investment_plans"),
    path("investment-history/", views.investment_history, name="investment_history"),
    path("investment-history/<int:investment_id>/", views.investment_detail, name="investment_detail"),
    path("payment-methods/", views.payment_methods, name="payment_methods"),

  
    path("management/withdrawals/", views.withdrawals, name="withdrawals"),
    path("management/withdrawals/<int:withdrawal_id>/update/", views.update_withdrawal_status, name="update_withdrawal_status"),

  
    path("verifications/", views.verifications, name="verifications"),
    path("verifications/<int:kyc_id>/approve/", views.approve_kyc, name="approve_kyc"),
    path("verifications/<int:kyc_id>/reject/", views.reject_kyc, name="reject_kyc"),
    path("login/", views.admin_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verify/<int:user_id>/", views.verify_user, name="verify_user"),

   
    path("users/", views.all_users, name="all_users"),
    path("users/<int:user_id>/update/", views.update_user, name="update_user"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
    path("users_json/", views.users_json, name="users_json"),

   
    path("investment-plans-admin/", views.admin_investment_plans, name="admin_investment_plans"),
    path("investment-plans-admin/<int:plan_id>/update/", views.update_investment_plan, name="update_investment_plan"),

  
    path("financials/", views.all_financials, name="all_financials"),
    path("management/deposits/<int:deposit_id>/update/", views.update_deposit_status, name="update_deposit_status"),
    path("transactions/", views.all_transactions, name="all_transactions"),
    path("wallets/", views.admin_wallets, name="admin_wallets"),
]

