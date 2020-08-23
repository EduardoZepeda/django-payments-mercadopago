# django-payments-mercadopago

A mercadopago payment gateway backend for [django-payments](https://github.com/mirumee/django-payments)

## Installation

You can install it via pip

```Shell
pip install django-payments-mercadopago
```

Add *payments_mercadopago* to your *settings.py* file

```python
INSTALLED_APPS = [
    # ...
    'payments_mercadopago',
    ]
```

## Settings.py configuration

Add the *payments_mercadopago.MercadoPagoProvider* to your *PAYMENT_VARIANTS* variable. Also to make it available add MercadoPago to your *CHECKOUT_PAYMENT_CHOICES variable*

Mercado Pago doesn't require you to specify a fixed sandbox endpoint, instead they provide you with a sandbox token and a production token, for testing and production, respectively.

### Configuration for development

```Python
PAYMENT_VARIANTS = {
    # ...
    'MercadoPago':('payments_mercadopago.MercadoPagoProvider',{
        'access_token': 'MERCADO_PAGO_SANDBOX_ACCESS_TOKEN',
        'sandbox_mode: True})
}

CHECKOUT_PAYMENT_CHOICES = [('MercadoPago', 'Mercado Pago')]
```

If you have any problem using localhost urls as the return value of get_failure_url() or get_success_url() methods try using [ngrok](https://ngrok.com/) instead.

### Configuration for production

```Python
PAYMENT_VARIANTS = {
    # ...
    'MercadoPago':('payments_mercadopago.MercadoPagoProvider',{
        'access_token': 'MERCADO_PAGO_ACCESS_TOKEN',
        'sandbox_mode: False})
}

CHECKOUT_PAYMENT_CHOICES = [('MercadoPago', 'Mercado Pago')]
```

## Obtaining the Tokens

You can get your own Mercado Pago production and sandbox access tokens in your [Mercado Pago developer panel](https://www.mercadopago.com.mx/developers/panel/credentials)


## Documentation

For detailed instructions on how to use django-payments please visit the official [django-payments documentation](https://django-payments.readthedocs.io/en/latest/)

