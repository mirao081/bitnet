from django import forms
from users.models import UserProfile
from users.models import CompanyWallet


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            "usd_balance",
            "profit_balance",
            "bonus_balance",
            "verification_status",
        ]

        widgets = {
            "usd_balance": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "USD Balance"
            }),
            "profit_balance": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Profit Balance"
            }),
            "bonus_balance": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Bonus Balance"
            }),
            "verification_status": forms.Select(attrs={
                "class": "form-control"
            }),
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
