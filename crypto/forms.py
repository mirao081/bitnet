from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox   # ✅ use checkbox widget

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    service = forms.ChoiceField(choices=[
        ('deposit', 'How to make deposit'),
        ('benefit', 'The best way to benefit from the platform'),
        ('withdrawals', 'Advisory on withdrawals'),
        ('wait', 'Minimum wait before withdrawal'),
        ('analysis', 'Crypto market analysis'),
        ('blockchain', 'Blockchain model'),
        ('legal', 'Legal advisory (KYC/AML, SEC etc)')
    ])
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)   # ✅ corrected

class StyledLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)   # ✅ corrected

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class StyledSignupForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)   # ✅ corrected

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
