import os

PROJECT_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), 'payments_mercadopago'))
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')]}]

SECRET_KEY = 'MY-SECRET-KEY'
PAYMENT_HOST = 'example.org'

INSTALLED_APPS = ['payments', 'django.contrib.sites']
ROOT_URLCONF = 'payments.urls'
