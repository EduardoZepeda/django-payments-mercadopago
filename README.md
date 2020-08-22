django-payments-mercadopago
===========================

A mercadopago payment gateway backend for [django-payments](https://github.com/mirumee/django-payments)

Installation
------------

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

Settings.py configuration
-------------------------

Add the *payments_mercadopago.MercadoPagoProvider* to your *PAYMENT_VARIANTS* variable. Also to make it available add MercadoPago to your *CHECKOUT_PAYMENT_CHOICES variable*

```Python
PAYMENT_VARIANTS = {
    # ...
    'MercadoPago':('payments_mercadopago.MercadoPagoProvider',{
        'access_token': 'MERCADO_PAGO_ACCESS_TOKEN',
        'init_point': 'sandbox_init_point'})
}

CHECKOUT_PAYMENT_CHOICES = [('MercadoPago', 'Mercado Pago')]
```

Mercado Pago doesn't require you to specify a sandbox endpoint, instead they provide you with a sandbox token and a production token, for testing and production, respectively.
You can get your own Mercado Pago production or sandbox access token in your [Mercado Pago developer panel](https://www.mercadopago.com.mx/developers/panel/credentials)


Usage
-----

For detailed instructions on how to use django-payments please visit the official [django-payments documentation](https://django-payments.readthedocs.io/en/latest/)
