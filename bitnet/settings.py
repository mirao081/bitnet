from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '$c_0uv_w&=4$0i_28-g#a15obq1@&7s0t1z&q4yglb1-##n5=7'
DEBUG = False
ALLOWED_HOSTS = ['gloria1231.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crypto',
    'users',
    'adminpanel',
    'django.contrib.humanize',
    'django_recaptcha',
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
        'DIRS': [BASE_DIR / "templates"],  # optional global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'crypto.context_processors.ticker_instruments',
                'crypto.context_processors.global_settings',
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

# Login flow
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/users/dashboard/'

# Static & media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'



# Tell Django where to find static files in your apps
STATICFILES_DIRS = [
    BASE_DIR / "crypto" / "static",
    BASE_DIR / "users" / "static",
    BASE_DIR / "adminpanel" / "static",
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = "6LfYRWotAAAAADZOYTAPexRxP48RWIDrfj7sCAaj"
RECAPTCHA_PRIVATE_KEY = "6LfYRWotAAAAAAUahZ20rCzW6f9ksHJyMfXsH9WV"
RECAPTCHA_USE_SSL = True

# Email
DEFAULT_FROM_EMAIL = "chineduarize4@gmail.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "chineduarize4@gmail.com"
EMAIL_HOST_PASSWORD = "ujoognwjzqnneolo"
