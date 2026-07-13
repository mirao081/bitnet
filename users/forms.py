from django import forms
from .models import UserKYC

class KYCForm(forms.ModelForm):
    class Meta:
        model = UserKYC
        fields = ['document']
        widgets = {
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
