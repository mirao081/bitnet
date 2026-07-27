from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import ActiveInvestment, UserBalance, Deposit, Withdrawal,UserKYC,UserVerification,Referral,CompanyWallet
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.db.models import Count
from users.models import Deposit, ActiveInvestment, Withdrawal,UserProfile,UserWallet
from decimal import Decimal, InvalidOperation
from crypto.models import InvestmentPlan,Wallet
from users.forms import UserWalletForm
from django.contrib.admin.views.decorators import staff_member_required






def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_deposits = sum(d.amount for d in Deposit.objects.all())
    total_investments = sum(inv.amount for inv in ActiveInvestment.objects.all())
    active_investments = ActiveInvestment.objects.filter(status="active").count()
    total_withdrawals = sum(w.amount for w in Withdrawal.objects.all())
    total_usd_balance = sum(p.usd_balance for p in UserProfile.objects.all())
    total_investment_balance = sum(p.investment_balance for p in UserProfile.objects.all())
    total_profit_balance = sum(p.profit_balance for p in UserProfile.objects.all())
    total_bonus_balance = sum(p.bonus_balance for p in UserProfile.objects.all())
    total_referral_bonus = sum(p.referral_bonus for p in UserProfile.objects.all())

    investment_list = ActiveInvestment.objects.order_by("-start_date")
    investment_paginator = Paginator(investment_list, 4)
    recent_investments = investment_paginator.get_page(request.GET.get("investment_page"))

    user_list_recent = User.objects.order_by("-date_joined")
    user_paginator_recent = Paginator(user_list_recent, 4)
    recent_users = user_paginator_recent.get_page(request.GET.get("user_page"))

    user_list_all = User.objects.order_by("-date_joined")
    user_paginator_all = Paginator(user_list_all, 10)
    all_users = user_paginator_all.get_page(request.GET.get("page"))

    query = request.GET.get("q", "")
    referrals = Referral.objects.select_related("user", "referrer")
    if query:
        referrals = referrals.filter(user__username__icontains=query) | referrals.filter(referrer__username__icontains=query)

    top_referrers = (
        Referral.objects.values("referrer__username")
        .annotate(total=Count("user"))
        .order_by("-total")[:5]
    )

    context = {
        "total_users": total_users,
        "total_deposits": round(total_deposits, 2),
        "total_investments": round(total_investments, 2),
        "active_investments": active_investments,
        "total_withdrawals": round(total_withdrawals, 2),
        "total_usd_balance": round(total_usd_balance, 2),
        "total_investment_balance": round(total_investment_balance, 2),
        "total_profit_balance": round(total_profit_balance, 2),
        "total_bonus_balance": round(total_bonus_balance, 2),
        "total_referral_bonus": round(total_referral_bonus, 2),

        "recent_investments": recent_investments,
        "recent_users": recent_users,
        "all_users": all_users,

        "referrals": referrals,
        "query": query,
        "top_referrers": top_referrers,
    }

    return render(request, "adminpanel/admin_dashboard.html", context)


def all_users(request):
    user_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(user_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "adminpanel/users.html", {"page_obj": page_obj})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "send_email":
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, "Email sent successfully!")

        elif action == "fund_account":
            try:
                amount = Decimal(request.POST.get("amount"))
            except (TypeError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
                return redirect("adminpanel:update_user", user_id=user.id)

            profile.usd_balance += amount
            profile.save()
            messages.success(request, f"Funded {user.username}'s account with ${amount}.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "debit_account":
            try:
                amount = Decimal(request.POST.get("amount"))
            except (TypeError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
                return redirect("adminpanel:update_user", user_id=user.id)

            if profile.usd_balance >= amount:
                profile.usd_balance -= amount
                profile.save()
                messages.success(request, f"Debited ${amount} from {user.username}'s account.")
            else:
                messages.error(request, "Insufficient balance to debit.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "add_investment":  
            try:
                amount = Decimal(request.POST.get("amount"))
            except (TypeError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
                return redirect("adminpanel:update_user", user_id=user.id)

            profile.investment_balance += amount
            profile.save()
            messages.success(request, f"Added ${amount} to {user.username}'s investment balance.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "add_profit":
            try:
                amount = Decimal(request.POST.get("amount"))
            except (TypeError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
                return redirect("adminpanel:update_user", user_id=user.id)

            profile.profit_balance += amount
            profile.save()
            messages.success(request, f"Added ${amount} profit to {user.username}.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "add_bonus":
            try:
                amount = Decimal(request.POST.get("amount"))
            except (TypeError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
                return redirect("adminpanel:update_user", user_id=user.id)

            profile.bonus_balance += amount
            profile.save()
            messages.success(request, f"Added ${amount} bonus to {user.username}.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "referral_bonus":
            try:
                amount = Decimal(request.POST.get("amount"))
            except (TypeError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
                return redirect("adminpanel:update_user", user_id=user.id)

            profile.referral_bonus += amount
            profile.save()
            messages.success(request, f"Added ${amount} referral bonus to {user.username}.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "verify_account":
            status = request.POST.get("status")
            profile.verification_status = status
            profile.save()
            messages.success(request, f"{user.username}'s account verification updated to {status}.")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "change_password":
            new_password = request.POST.get("new_password")
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect("adminpanel:update_user", user_id=user.id)

        elif action == "login_as_user":
            login(request, user)
            return redirect("users:dashboard")

        elif action == "delete_user":
            user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect("adminpanel:all_users")

    return render(request, "adminpanel/user_detail.html", {"user": user, "profile": profile})


@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "adminpanel/user_detail.html", context)




@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def verify_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.profile.is_verified = True
    user.profile.save()
    return redirect('adminpanel:dashboard')



def investment_history(request):
    investments_list = ActiveInvestment.objects.select_related("user").all().order_by("-start_date")
    paginator = Paginator(investments_list, 5)
    page_number = request.GET.get("page")
    investments = paginator.get_page(page_number)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for inv in investments:
            data.append({
                "id": inv.id,
                "username": inv.user.username,
                "plan_name": inv.plan_name,
                "amount": str(inv.amount),
                "roi_percent": str(inv.roi_percent),
                "start_date": inv.start_date.strftime("%Y-%m-%d"),
                "end_date": inv.end_date.strftime("%Y-%m-%d"),
            })
        return JsonResponse({
            "investments": data,
            "has_next": investments.has_next(),
            "has_previous": investments.has_previous(),
            "page": investments.number,
            "num_pages": investments.paginator.num_pages,
        })

    return render(request, "adminpanel/investment_history.html", {"investments": investments})


def update_investment_plan(request, investment_id):
    investment = get_object_or_404(ActiveInvestment, id=investment_id)
    if request.method == "POST":
       
        investment.save()
       
        page_number = request.GET.get("page", 1)
        return redirect(f"/adminpanel/investment-history/?page={page_number}#inv-{investment.id}")
    return redirect("adminpanel:investment_history")


def investment_detail(request, investment_id):
    investment = get_object_or_404(ActiveInvestment, id=investment_id)
    trades = [investment]  
    paginator = Paginator(trades, 5)
    page_number = request.GET.get("page")
    trades_page = paginator.get_page(page_number)

    return render(request, "adminpanel/investment_detail.html", {"investment": investment, "trades": trades_page})




def payment_methods(request):
    wallet, created = UserWallet.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserWalletForm(request.POST, request.FILES, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:payment_methods")
    else:
        form = UserWalletForm(instance=wallet)
    return render(request, "adminpanel/payment_methods.html", {"form": form, "wallet": wallet})



@staff_member_required
def all_financials(request):
    search_query = request.GET.get("q", "")

    # Get deposits
    deposits = Deposit.objects.select_related("user").order_by("-created_at")
    if search_query:
        deposits = deposits.filter(user__username__icontains=search_query)

    # Get investments
    investments = ActiveInvestment.objects.select_related("user").order_by("-start_date")
    if search_query:
        investments = investments.filter(user__username__icontains=search_query)

    combined = []
    for d in deposits:
        combined.append({
            "id": d.id,
            "type": "Deposit",
            "user": d.user.username,
            "amount": d.amount,
            "status": d.status,
            "date": d.created_at,
        })
    for inv in investments:
        combined.append({
            "id": inv.id, 
            "type": "Investment",
            "user": inv.user.username,
            "amount": inv.amount,
            "status": inv.status,
            "date": inv.start_date,
        })

   
    combined.sort(key=lambda x: x["date"], reverse=True)
    paginator = Paginator(combined, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "adminpanel/financials.html", {
        "page_obj": page_obj,
        "search_query": search_query,
    })


@staff_member_required
def update_deposit_status(request, deposit_id):
    if request.method == "POST":
        status = request.POST.get("status")
        deposit = Deposit.objects.get(id=deposit_id)
        if status in ["pending", "approved", "fail"]:
            deposit.status = status
            deposit.save()
            messages.success(request, "Deposit status updated.")
    return redirect("adminpanel:all_financials")

def withdrawals(request):
   
    search_query = request.GET.get("q", "")

    
    withdrawals_qs = Withdrawal.objects.all().order_by("-created_at")
    if search_query:
        withdrawals_qs = withdrawals_qs.filter(user__username__icontains=search_query)

  
    paginator = Paginator(withdrawals_qs, 3)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "adminpanel/withdrawals.html", {
        "page_obj": page_obj,
        "search_query": search_query,
    })

def update_withdrawal_status(request, withdrawal_id):
    withdrawal = get_object_or_404(Withdrawal, id=withdrawal_id)
    if request.method == "POST":
        status = request.POST.get("status")
        if status:
            withdrawal.status = status
            withdrawal.save()
            messages.success(request, "Withdrawal update.")
    return redirect("adminpanel:withdrawals")


@login_required
def all_transactions(request):

    deposits = Deposit.objects.select_related("user").all()
    withdrawals = Withdrawal.objects.select_related("user").all()
    active_investments = ActiveInvestment.objects.select_related("user").all()

    transactions = []
    for d in deposits:

        wallet = "No wallet yet"

        try:
            uw = d.user.userwallet

            if d.currency == "BTC":
                wallet = uw.btc_wallet or "No wallet yet"

            elif d.currency == "ETH":
                wallet = uw.eth_wallet or "No wallet yet"

            elif d.currency == "USDT_ERC20":
                wallet = uw.usdt_erc20_wallet or "No wallet yet"

            elif d.currency == "USDT_TRC20":
                wallet = uw.usdt_trc20_wallet or "No wallet yet"

        except UserWallet.DoesNotExist:
            pass

        transactions.append({
            "date": d.created_at,
            "username": d.user.username,
            "type": "Deposit",
            "currency": d.currency,
            "amount": d.amount,
            "wallet_address": wallet,
            "status": d.status,
        })

    for w in withdrawals:

        transactions.append({
            "date": w.created_at,
            "username": w.user.username,
            "type": "Withdrawal",
            "currency": w.currency,
            "amount": w.amount,
            "wallet_address": w.wallet_address or "No wallet yet",
            "status": w.status,
        })

    for inv in active_investments:

        wallet = "No wallet yet"

        try:
            uw = inv.user.userwallet

            if inv.currency == "BTC":
                wallet = uw.btc_wallet or "No wallet yet"

            elif inv.currency == "ETH":
                wallet = uw.eth_wallet or "No wallet yet"

            elif inv.currency == "USDT_ERC20":
                wallet = uw.usdt_erc20_wallet or "No wallet yet"

            elif inv.currency == "USDT_TRC20":
                wallet = uw.usdt_trc20_wallet or "No wallet yet"

        except UserWallet.DoesNotExist:
            pass

        transactions.append({
            "date": inv.start_date,
            "username": inv.user.username,
            "type": "Investment",
            "currency": inv.currency,
            "amount": inv.amount,
            "wallet_address": wallet,
            "status": inv.status,
        })
    transactions.sort(key=lambda x: x["date"], reverse=True)
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "adminpanel/all_transactions.html",
        {
            "page_obj": page_obj
        }
    )

def verifications(request):
    verifications_list = UserKYC.objects.all().order_by("-submitted_at")
    paginator = Paginator(verifications_list, 5)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "adminpanel/verifications.html", {"page_obj": page_obj})

def approve_kyc(request, kyc_id):
    kyc = get_object_or_404(UserKYC, id=kyc_id)
    kyc.status = "approved"
    kyc.save()

    user_verification, created = UserVerification.objects.get_or_create(user=kyc.user)
    user_verification.is_verified = True
    user_verification.save()

    messages.success(request, f"KYC for {kyc.user.username} approved and user verified.")
    return redirect("adminpanel:verifications")


def reject_kyc(request, kyc_id):
    kyc = get_object_or_404(UserKYC, id=kyc_id)
    kyc.status = "rejected"
    kyc.save()

    user_verification, created = UserVerification.objects.get_or_create(user=kyc.user)
    user_verification.is_verified = False
    user_verification.save()

    messages.error(request, f"KYC for {kyc.user.username} rejected and user not verified.")
    return redirect("adminpanel:verifications")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect("adminpanel:dashboard")

        return render(
            request,
            "adminpanel/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "adminpanel/login.html")

@login_required
def users_json(request):
    page_number = request.GET.get("page", 1)
    all_users = User.objects.all().order_by("id")
    paginator = Paginator(all_users, 10)  
    page_obj = paginator.get_page(page_number)

    data = {
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "balance": str(getattr(getattr(u, "userprofile", None), "usd_balance", "0.00")),
                # If referrer is a User object, convert to username or id
                "referrer": getattr(getattr(u, "userprofile", None), "referrer", None).username 
                            if getattr(getattr(u, "userprofile", None), "referrer", None) else None,
                "status": getattr(getattr(u, "userprofile", None), "verification_status", "pending"),
                "date_joined": u.date_joined.strftime("%Y-%m-%d"),
            }
            for u in page_obj
        ],
        "page_number": page_obj.number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }
    return JsonResponse(data)

@login_required
def admin_investment_plans(request):
    plans = InvestmentPlan.objects.all()
    return render(request, "adminpanel/investment_plans.html", {"plans": plans})

@login_required
def update_investment_plan(request, plan_id):
    plan = get_object_or_404(InvestmentPlan, id=plan_id)
    if request.method == "POST":
        plan.name = request.POST.get("name")
        plan.percentage_text = request.POST.get("percentage_text")
        plan.roi_percent = request.POST.get("roi_percent")
        plan.duration_text = request.POST.get("duration_text")
        plan.duration_hours = request.POST.get("duration_hours")
        plan.maturity_text = request.POST.get("maturity_text")
        plan.min_amount = request.POST.get("min_amount")
        plan.max_amount = request.POST.get("max_amount")
        plan.save()

        messages.success(request, f"Investment plan '{plan.name}' updated successfully.")
        return redirect(f"/adminpanel/investment-plans#plan-{plan.id}")

    return redirect("adminpanel:admin_investment_plans")



def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def referral_dashboard(request):
    query = request.GET.get("q", "")
    referrals_qs = Referral.objects.select_related("user", "referrer")

    if query:
        referrals_qs = referrals_qs.filter(user__username__icontains=query) | referrals_qs.filter(referrer__username__icontains=query)

    # Add pagination
    paginator = Paginator(referrals_qs, 10)  # show 10 records per page
    page_number = request.GET.get("page")
    referrals = paginator.get_page(page_number)

    context = {
        "referrals": referrals,
        "query": query,
    }
    return render(request, "adminpanel/admin_dashboard.html", context)


@login_required
def create_wallet(request):
    user = request.user
    plans = InvestmentPlan.objects.all()

    if request.method == "POST":
        plan_id = request.POST.get("plan")
        plan = InvestmentPlan.objects.get(id=plan_id)

        wallet, created = Wallet.objects.get_or_create(user=user, defaults={"plan": plan})
        if not created:
            wallet.plan = plan
        wallet.deduct_gas_fee()
        return redirect("wallets")  # redirect to your wallets dashboard

    return render(request, "users/create_wallet.html", {"plans": plans})

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_wallets(request):
    wallets = Wallet.objects.select_related("user", "plan").all()
    return render(request, "adminpanel/wallets.html", {"wallets": wallets})

def logout_view(request):
    logout(request)
    return redirect("adminpanel:login")
