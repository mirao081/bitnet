from django import forms
from .models import UserKYC, UserWallet, UserVerification, APIKey, UserProfile,Withdrawal
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from users.models import CompanyWallet

class KYCForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = UserKYC
        fields = ['document', 'captcha']
        widgets = {
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UserWalletForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = UserWallet
        fields = [
            "btc_wallet", "btc_qr",
            "eth_wallet", "eth_qr",
            "usdt_erc20_wallet", "usdt_erc20_qr",
            "usdt_trc20_wallet", "usdt_trc20_qr",
            "captcha"
        ]

class ProfileForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = UserProfile
        fields = [
            "phone", "profile_picture", "country", "timezone",
            "risk_level", "preferred_assets", "auto_invest", "captcha"
        ]

class NotificationsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = UserProfile
        fields = ["email_notifications", "sms_notifications", "captcha"]

class AccountForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = UserProfile
        fields = ["is_deactivated", "export_requested", "captcha"]

class VerificationForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = UserVerification
        fields = ["is_verified", "captcha"]

class APIForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = APIKey
        fields = ["status", "captcha"]

class SettingsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = User
        fields = ["username", "email", "captcha"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "settings-input", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "settings-input", "placeholder": "Email"}),
        }


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = [
            "currency",
            "amount",
            "wallet_address",
        ]

        widgets = {
            "currency": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter withdrawal amount"
                }
            ),

            "wallet_address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter destination wallet address"
                }
            ),
        }


class CompanyWalletForm(forms.ModelForm):
    class Meta:
        model = CompanyWallet
        fields = [
            "btc_wallet", "btc_qr",
            "eth_wallet", "eth_qr",
            "usdt_erc20_wallet", "usdt_erc20_qr",
            "usdt_trc20_wallet", "usdt_trc20_qr",
        ]
