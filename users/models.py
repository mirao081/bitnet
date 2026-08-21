from django.db import models
from django.contrib.auth.models import User
import secrets
from django.utils import timezone
from decimal import Decimal
import re


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} Balance"


class ActiveInvestment(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
    ]

    CURRENCY_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_ERC20", "USDT ERC20"),
        ("USDT_TRC20", "USDT TRC20"),
        ("USD", "USD"),
    ]

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    plan_name = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=20,
        choices=CURRENCY_CHOICES,
        default="USD"
    )

    roi_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"

    def get_current_multiplier(self):
        now = timezone.now()

        if now >= self.end_date:
            return Decimal("1") + (self.roi_percent / Decimal("100"))

        total_duration = Decimal(
            (self.end_date - self.start_date).total_seconds()
        )

        elapsed = Decimal(
            (now - self.start_date).total_seconds()
        )

        progress = elapsed / total_duration

        return Decimal("1") + (
            self.roi_percent / Decimal("100")
        ) * progress

    def get_current_value(self):
        return self.amount * self.get_current_multiplier()
    
class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referrer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals"
    )

    def __str__(self):
        return f"{self.user.username} was referred by {self.referrer.username if self.referrer else 'None'}"

    @property
    def referral_count(self):
       
        return Referral.objects.filter(referrer=self.user).count()


    
class ReferralCommission(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commissions")
    referral = models.ForeignKey(User, on_delete=models.CASCADE, related_name="generated_commissions")
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.username} earned ${self.commission_amount} from {self.referral.username}"
    

class Deposit(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
    ]

    CURRENCY_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_ERC20", "USDT ERC20"),
        ("USDT_TRC20", "USDT TRC20"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    bonus_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Restrict deposits unless user is verified
        if self.user.userprofile.verification_status != "verified":
            raise PermissionError("Admin must verify your account before deposits.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Deposit {self.amount}"
    
class CompanyWallet(models.Model):
    btc_wallet = models.CharField(max_length=200, blank=True, null=True)
    btc_qr = models.ImageField(upload_to="company_wallets/", blank=True, null=True)

    eth_wallet = models.CharField(max_length=200, blank=True, null=True)
    eth_qr = models.ImageField(upload_to="company_wallets/", blank=True, null=True)

    usdt_erc20_wallet = models.CharField(max_length=200, blank=True, null=True)
    usdt_erc20_qr = models.ImageField(upload_to="company_wallets/", blank=True, null=True)

    usdt_trc20_wallet = models.CharField(max_length=200, blank=True, null=True)
    usdt_trc20_qr = models.ImageField(upload_to="company_wallets/", blank=True, null=True)

    def __str__(self):
        return "Company Wallets"


class Withdrawal(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("rejected", "Rejected"),
    ]

    CURRENCY_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_ERC20", "USDT ERC20"),
        ("USDT_TRC20", "USDT TRC20"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="withdrawals"
    )

    currency = models.CharField(
        max_length=20,
        choices=CURRENCY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    wallet_address = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    txid = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    admin_note = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.currency} - {self.amount}"
    
class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    secret = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.is_verified else 'Not Verified'}"


class UserKYC(models.Model):
    STATUS_CHOICES = [
        ('pending', 'KYC Pending'),
        ('approved', 'KYC Approved'),
        ('rejected', 'KYC Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    document = models.FileField(upload_to='kyc_documents/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"


class RecoveryCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.code} ({'used' if self.used else 'active'})"


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    device = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="Successful")

    def __str__(self):
        return f"{self.user.username} - {self.device} - {self.status}"


class SecurityAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"{self.user.username} - {self.event} ({self.status})"

class Notification(models.Model):
    TYPE_CHOICES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("admin", "Admin"),
        ("promotion", "Promotion"),
        ("signup", "Signup"),
        ("verification", "Verification"),
        ("investment", "Investment"),
        ("referral", "Referral"),
        ("bonus", "Bonus"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.message[:30]}"


class SupportArticle(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("account", "Account"),
        ("investment", "Investment"),
        ("security", "Security"),
        ("withdrawal", "Withdrawal"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="general")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.title}"


class UserWallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="userwallet"
    )
    
    usd_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    btc_balance = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    eth_balance = models.DecimalField(max_digits=12, decimal_places=8, default=0)


    btc_wallet = models.CharField(max_length=100, blank=True, null=True)
    eth_wallet = models.CharField(max_length=100, blank=True, null=True)
    usdt_erc20_wallet = models.CharField(max_length=100, blank=True, null=True)
    usdt_trc20_wallet = models.CharField(max_length=100, blank=True, null=True)

    btc_qr = models.ImageField(upload_to="wallet_qrcodes/", blank=True, null=True)
    eth_qr = models.ImageField(upload_to="wallet_qrcodes/", blank=True, null=True)
    usdt_erc20_qr = models.ImageField(upload_to="wallet_qrcodes/", blank=True, null=True)
    usdt_trc20_qr = models.ImageField(upload_to="wallet_qrcodes/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Wallets"


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = secrets.token_hex(16)  

    def __str__(self):
        return f"{self.user.username} - {self.value[:6]}..."


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)

    referrer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_referrals"
    )
    

    risk_level = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium"
    )
    preferred_assets = models.TextField(blank=True, null=True)
    auto_invest = models.BooleanField(default=False)

   
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

   
    is_deactivated = models.BooleanField(default=False)
    export_requested = models.BooleanField(default=False)

  
    usd_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    btc_balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    eth_balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)

    
    usdt_erc20_balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    usdt_trc20_balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)

  
    btc_address = models.CharField(max_length=255, blank=True, null=True)
    eth_address = models.CharField(max_length=255, blank=True, null=True)
    usdt_erc20_address = models.CharField(max_length=255, blank=True, null=True)
    usdt_trc20_address = models.CharField(max_length=255, blank=True, null=True)

  
    investment_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    profit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    referral_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)

   
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("request_document", "Request Document"),
            ("verified", "Verified"),
            ("update_billing", "Update Billing"),
        ],
        default="pending"
    )

    def __str__(self):
        return f"{self.user.username} Profile"
    
class Transaction(models.Model):
    TYPE_CHOICES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("investment", "Investment"),
        ("payout", "Payout"),
        ("bonus", "Bonus"),
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    asset = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True) 
    created_at = models.DateTimeField(auto_now_add=True)  
    status = models.CharField(max_length=20, default="completed")

    def __str__(self):
        return f"{self.user.username} - {self.type} {self.amount} {self.asset}"


    
class ProfitRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profits")
    investment_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ("Credited", "Credited"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
    ], default="Credited")

    def __str__(self):
        return f"{self.user.username} - {self.investment_name} - ${self.amount}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.asset}"
    

