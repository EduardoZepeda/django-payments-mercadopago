from django.urls import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from decimal import Decimal, ROUND_HALF_UP
import json
import logging
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from payments import PaymentError, PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url

import mercadopago

CENTS = Decimal('0.01')

logger = logging.getLogger(__name__)


class MercadoPagoProvider(BasicProvider):

    def __init__(self, access_token, sandbox_mode=False, **kwargs):
        self.access_token = access_token
        self.sandbox_mode = sandbox_mode
        self.init_point = 'sandbox_init_point' if self.sandbox_mode else 'init_point'
        self.mp = mercadopago.MP(self.access_token)
        self.mp.sandbox_mode(self.sandbox_mode)
        super(MercadoPagoProvider, self).__init__(**kwargs)

    def get_form(self, payment, data=None, file_data=None):
        if not payment.id:
            payment.save()
        payment_data = self.create_payment(payment)
        redirect_to = self.get_value_from_response(
            payment_data, self.init_point)
        payment.change_status(PaymentStatus.WAITING)
        raise RedirectNeeded(redirect_to)

    def create_payment(self, payment):
        preference = self.create_preference_data(payment)
        preferenceResult = self.mp.create_preference(preference)
        payment.extra_data = json.dumps(preferenceResult)
        if 200 <= preferenceResult['status'] <= 201:
            return preferenceResult
        message = self.get_value_from_response(preferenceResult, 'message')
        logger.warning(message, extra={"response": preferenceResult})
        raise PaymentError(message)

    def get_value_from_response(self, response, key):
        return response.get('response', {}).get(key, {})

    def create_notification_url(self, payment):
        return urljoin(get_base_url(), reverse('process_payment',
                                               kwargs={"token": payment.token}))

    def create_preference_data(self, payment):
        items = list(self.get_transactions_items(payment))
        items.insert(
            0, self.get_order_name_and_shipping_cost(payment))
        sub_total = (
            payment.total - payment.delivery - payment.tax)
        sub_total = sub_total.quantize(CENTS, rounding=ROUND_HALF_UP)
        total = payment.total.quantize(CENTS, rounding=ROUND_HALF_UP)
        tax = payment.tax.quantize(CENTS, rounding=ROUND_HALF_UP)
        delivery = payment.delivery.quantize(
            CENTS, rounding=ROUND_HALF_UP)
        full_name = payment.billing_first_name + " " \
            + payment.billing_last_name
        full_address = payment.billing_address_1 + " " \
            + payment.billing_address_2
        # Please check the preferences API for customization
        # www.mercadopago.com.mx/developers/es/reference/preferences/resource/
        preferenceData = {
            "items": items,
            "payer": {
                "name": full_name,
                "email": payment.billing_email,
                "address": {
                    "street_name": full_address,
                    "zip_code": payment.billing_postcode
                },
            },

            "back_urls": {
                # Localhost urls raise an error in payment in
                # mercadopago website, even in sandbox mode
                # When testing in localhost use Ngrok instead
                "success": payment.get_success_url(),
                "failure": payment.get_failure_url(),
                "pending": payment.get_failure_url(),
            },
            "auto_return": "approved",
            "notification_url": self.create_notification_url(payment),
            "external_reference": payment.token,
        }
        return preferenceData

    def get_transactions_items(self, payment):
        for purchased_item in payment.get_purchased_items():
            price = purchased_item.price.quantize(
                CENTS, rounding=ROUND_HALF_UP)
            item = {'title': purchased_item.name[:127],
                    'quantity': purchased_item.quantity,
                    'unit_price': float(price),
                    'currency_id': purchased_item.currency,
                    'id': purchased_item.sku}
            yield item

    def get_order_name_and_shipping_cost(self, payment):
        item = {'title': payment.description + _(' and shipping'),
                'quantity': 1,
                'unit_price': float(payment.delivery),
                'currency': payment.currency,
                'id': _('shipping')
                }
        return item

    def process_payment_data_received(self, payment, collection_id):
        payment_information = self.get_payment_information(collection_id)
        payment.transaction_id = collection_id
        payment.extra_data = json.dumps(payment_information)
        return payment_information

    def set_payment_status(self, payment, payment_status):
        if payment_status == 'approved':
            payment.captured_amount = payment.total
            payment.change_status(PaymentStatus.CONFIRMED)
        else:
            payment.change_status(PaymentStatus.WAITING)

    def process_data(self, payment, request):
        if all(['data.id' in request.GET, 'type' in request.GET, request.GET.get('type') == 'payment']):
            collection_id = request.GET.get('data.id')
            payment_information = self.process_payment_data_received(
                payment, collection_id)
            payment_status = self.get_value_from_response(
                payment_information, "status")
            self.set_payment_status(payment, payment_status)
        return HttpResponse(status=200)

    def get_payment_information(self, payment_id):
        paymentInfo = self.mp.get_payment(payment_id)
        if paymentInfo["status"] == 200:
            return paymentInfo
        message = self.get_value_from_response(paymentInfo, 'message')
        logger.warning(message, extra={"response": paymentInfo})
        raise PaymentError(message)

    def refund(self, payment, amount=None):
        amount = payment.captured_amount
        # MercadoPago Official Python SDK doesn't support partial refunds
        refundResult = self.mp.refund_payment(payment.transaction_id)
        payment.extra_data = json.dumps(refundResult)
        if refundResult['status'] == 201:
            payment.change_status(PaymentStatus.REFUNDED)
            return amount
        message = self.get_value_from_response(refundResult, 'message')
        raise PaymentError(message)

    def cancel(self, payment):
        cancelationResult = self.mp.cancel_payment(payment.transaction_id)
        payment.extra_data = json.dumps(cancelationResult)
        if cancelationResult['status'] == 200:
            payment.change_status(PaymentStatus.REJECTED)
        message = self.get_value_from_response(cancelationResult, 'message')
        logger.warning(message, extra={"response": cancelationResult})
        raise PaymentError(message)
