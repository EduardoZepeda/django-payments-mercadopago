===========================
django-payments-mercadopago
===========================

A mercadopago payment gateway backend for `django-payments <https://github.com/mirumee/django-payments>`_

Compatibility
-------------

* Python 3.6 ≥ 3.8
* Django 2.2 ≥ 3.2


Installation
------------

You can install it via pip, pipenv or your favorite virtual environment manager

.. code-block:: bash

  pip install django-payments-mercadopago

Add *payments_mercadopago* to your *settings.py* file

.. code-block:: python

  INSTALLED_APPS = [
      # ...
      'payments_mercadopago',
      ]

Settings.py configuration
-------------------------

Add the *payments_mercadopago.MercadoPagoProvider* to your *PAYMENT_VARIANTS* variable. Also to make it available add MercadoPago to your *CHECKOUT_PAYMENT_CHOICES variable*

Configuration for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  PAYMENT_VARIANTS = {
      # ...
      'MercadoPago':('payments_mercadopago.MercadoPagoProvider',{
          'access_token': 'MERCADO_PAGO_SANDBOX_ACCESS_TOKEN',
          'sandbox_mode': True})
  }

  CHECKOUT_PAYMENT_CHOICES = [('MercadoPago', 'Mercado Pago')]

If you have any problem using localhost urls as the return value of get_failure_url() or get_success_url() methods try using `ngrok <https://ngrok.com>`_.

Configuration for production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

  PAYMENT_VARIANTS = {
      # ...
      'MercadoPago':('payments_mercadopago.MercadoPagoProvider',{
          'access_token': 'MERCADO_PAGO_ACCESS_TOKEN',
          'sandbox_mode': False})
  }

  CHECKOUT_PAYMENT_CHOICES = [('MercadoPago', 'Mercado Pago')]

Obtaining the Tokens
--------------------

You can get your own Mercado Pago production and sandbox access tokens in your `Mercado pago developer panel <https://www.mercadopago.com/developers/panel/credentials>`_


Documentation
-------------

This project uses django-payments to work. For detailed instructions on how to make and configure payments using django-payments please visit the official `django-payments documentation <https://django-payments.readthedocs.io/en/latest/>`_
