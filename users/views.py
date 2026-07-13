from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from crypto.models import MarketInstrument
from .models import UserBalance, ActiveInvestment, Referral, UserKYC,Notification
from .forms import KYCForm
import json
import requests
from django.utils.timezone import now

@login_required
def dashboard(request):
    instruments = MarketInstrument.objects.all()
    balance = UserBalance.objects.filter(user=request.user).first()
    investments = ActiveInvestment.objects.filter(user=request.user)
    referral = Referral.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(user=request.user).order_by("-timestamp")[:10]

    # Growth chart: cumulative invested amounts by start_date
    growth_data = []
    growth_labels = []
    total = 0
    for inv in investments.order_by("start_date"):
        total += float(inv.amount)
        growth_data.append(total)
        growth_labels.append(inv.start_date.strftime("%b %d"))

    # ROI chart: simple calculation based on duration
    daily_roi = 0
    weekly_roi = 0
    monthly_roi = 0
    for inv in investments:
        days = (inv.end_date - inv.start_date).days
        if days > 0:
            daily_roi += float(inv.amount) / days
            weekly_roi += (float(inv.amount) / days) * 7
            monthly_roi += (float(inv.amount) / days) * 30

    roi_data = [round(daily_roi, 2), round(weekly_roi, 2), round(monthly_roi, 2)]

    # Market Insights: fetch live BTC, ETH, and S&P 500
    try:
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        crypto_data = requests.get(crypto_url).json()
        btc_price = crypto_data['bitcoin']['usd']
        eth_price = crypto_data['ethereum']['usd']

        fmp_url = "https://financialmodelingprep.com/api/v3/quote/%5EGSPC?apikey=ZR8hDHF0vtAETUxVCfT41Du5Wtc9fzEO"
        sp500_data = requests.get(fmp_url).json()
        sp500_index = sp500_data[0]['price']
    except Exception:
        btc_price = eth_price = sp500_index = "N/A"

    return render(request, "users/dashboard.html", {
        "instruments": instruments,
        "balance": balance,
        "investments": investments,
        "referral": referral,
        "growth_data": json.dumps(growth_data),
        "growth_labels": json.dumps(growth_labels),
        "roi_data": json.dumps(roi_data),
        "notifications": notifications,
        "btc_price": btc_price,
        "eth_price": eth_price,
        "sp500_index": sp500_index,
    })

@login_required
def portfolio(request):
    btc_balance = 0.5
    eth_balance = 2.0
    usdt_balance = 1000

    holdings = {
        "BTC": btc_balance,
        "ETH": eth_balance,
        "USDT": usdt_balance,
    }

    investments = ActiveInvestment.objects.filter(user=request.user)

    return render(request, "users/portfolio.html", {
        "holdings": holdings,
        "investments": investments,
    })

@login_required
def investments(request):
    return render(request, "users/investments.html")


@login_required
def investment_plans(request):
    return render(request, "users/investment_plans.html")


@login_required
def wallets(request):
    return render(request, "users/wallets.html")


@login_required
def deposit(request):
    return render(request, "users/deposit.html")


@login_required
def withdraw(request):
    return render(request, "users/withdraw.html")


@login_required
def transactions(request):
    return render(request, "users/transactions.html")


@login_required
def profit_history(request):
    return render(request, "users/profit_history.html")


@login_required
def referrals(request):
    return render(request, "users/referrals.html")


@login_required
def markets(request):
    return render(request, "users/markets.html")


@login_required
def news(request):
    return render(request, "users/news.html")


@login_required
def support(request):
    return render(request, "users/support.html")


@login_required
def profile(request):
    return render(request, "users/profile.html")


@login_required
def security(request):
    return render(request, "users/security.html")


@login_required
def settings(request):
    return render(request, "users/settings.html")


@login_required
def kyc_upload(request):
    kyc, created = UserKYC.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            form.save()
            kyc.status = 'pending'  
            kyc.save()
            return redirect('users:dashboard')
    else:
        form = KYCForm(instance=kyc)
    return render(request, 'users/kyc_upload.html', {'form': form, 'kyc': kyc})


@login_required
def ai_chat(request):
    return render(request, "users/ai_chat.html")


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")  

@login_required
def make_deposit(request):
    return render(request, "users/make_deposit.html")

@login_required
def request_withdrawal(request):
    return render(request, "users/request_withdrawal.html")

@login_required
def start_investment(request):
    return render(request, "users/start_investment.html")