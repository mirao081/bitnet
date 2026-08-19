from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '$c_0uv_w&=4$0i_28-g#a15obq1@&7s0t1z&q4yglb1-##n5=7'
DEBUG = False
ALLOWED_HOSTS = [
    'bitnetapp.com',
    'www.bitnetapp.com',
    'bitnethub.online',
    'www.bitnethub.online',
    '191.215.39.223',
    '127.0.0.1',
    'localhost',
]

CSRF_TRUSTED_ORIGINS = [
    'https://bitnetapp.com',
    'https://www.bitnetapp.com',
    'https://bitnethub.online',
    'https://www.bitnethub.online',
]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crypto.apps.CryptoConfig',
    'users.apps.UsersConfig',
    'adminpanel.apps.AdminpanelConfig',
    'django.contrib.humanize',
    'django_recaptcha',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bitnet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'crypto.context_processors.ticker_instruments',
                'crypto.context_processors.global_settings',
                'crypto.context_processors.recaptcha_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'bitnet.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🔑 Login settings
# Regular users log in via crypto app (/login/)
LOGIN_URL = '/login/'
# After login, users go to their dashboard
LOGIN_REDIRECT_URL = '/users/dashboard/'
# After logout, redirect back to login
LOGOUT_REDIRECT_URL = '/login/'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / "crypto" / "static",
    BASE_DIR / "users" / "static",
    BASE_DIR / "adminpanel" / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔑 reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = "6LebNoctAAAAAAaNs4Ykdrc8yQCZOs2TuDbxbZvu"
RECAPTCHA_PRIVATE_KEY = "6LebNoctAAAAAJv_88a_-8fUXDiCDX1wvA9t4fjZ"
RECAPTCHA_USE_SSL = True

# ✅ Default sender identity
DEFAULT_FROM_EMAIL = "Bitnet <support@bitnetapp.com>"

# ✅ Primary backend: SendGrid (default)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"   # SendGrid requires "apikey" here
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")  # store securely in env var

# ✅ Helper dict for signals that call send_html_email
SENDGRID_EMAIL_BACKEND = {
    "EMAIL_BACKEND": EMAIL_BACKEND,
    "EMAIL_HOST": EMAIL_HOST,
    "EMAIL_PORT": EMAIL_PORT,
    "EMAIL_USE_TLS": EMAIL_USE_TLS,
    "EMAIL_HOST_USER": EMAIL_HOST_USER,
    "EMAIL_HOST_PASSWORD": EMAIL_HOST_PASSWORD,
}

# 🔧 Optional: Zoho backend (kept for fallback/testing)
ZOHO_EMAIL_BACKEND = {
    "DEFAULT_FROM_EMAIL": "support@bitnetapp.com",
    "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
    "EMAIL_HOST": "smtp.zoho.com",
    "EMAIL_PORT": 587,
    "EMAIL_USE_TLS": True,
    "EMAIL_HOST_USER": "support@bitnetapp.com",
    "EMAIL_HOST_PASSWORD": os.getenv("ZOHO_EMAIL_PASSWORD"),
}
