from __future__ import unicode_literals
import json
from decimal import Decimal
from unittest import TestCase
from mock import patch, MagicMock, Mock

from django.http import HttpResponse
from django.utils import timezone

from . import MercadoPagoProvider
from payments import PurchasedItem, RedirectNeeded, PaymentError, PaymentStatus

CLIENT_ID = 'Mercado Pago Test User'
PAYMENT_TOKEN = '5a4dae68-2715-4b1e-8bb2-2c2dbe9255f6'
ACCESS_TOKEN = 'TEST_123456789ABCDEFGHIJKLM'
INIT_POINT = 'sandbox_init_point'
SANDBOX_INIT_POINT_URL = 'http://sandbox.mercadopago.com/redirecttopayment'
INIT_POINT_URL = 'http://mercadopago.com/redirecttopayment'
VARIANT = 'wallet'
CURRENCY = 'MXN'

class Payment(Mock):
    id = 1
    description = 'payment'
    currency = CURRENCY
    delivery = Decimal(10)
    status = PaymentStatus.WAITING
    tax = Decimal(10)
    token = PAYMENT_TOKEN
    total = Decimal(100)
    captured_amount = Decimal(0)
    variant = VARIANT
    transaction_id = None
    message = ''
    extra_data = {}
    billing_first_name = 'John'
    billing_last_name = 'Doe'
    billing_email = 'false@email.com'
    billing_address_1 = 'false st'
    billing_address_2 = '111'
    billing_postcode = '00000'

    def change_status(self, status, message=''):
        self.status = status
        self.message = message

    def get_failure_url(self):
        return 'http://cancel.com'

    def get_process_url(self):
        return 'http://example.com'

    def get_purchased_items(self):
        return [
            PurchasedItem(
                name='foo', quantity=Decimal('10'), price=Decimal('20'),
                currency='MXN', sku='bar')]

    def get_success_url(self):
        return 'http://success.com'

class TestMercadoPagoProvider(TestCase):

    def setUp(self):
        self.payment = Payment()
        self.provider = MercadoPagoProvider(
            access_token=ACCESS_TOKEN, sandbox_mode=True)

    @patch('mercadopago.MP.create_preference')
    def test_provider_raises_redirect_needed_on_success_preference_creation(
            self, mocked_create_preference):
        mocked_create_preference.return_value = {
            'status': 201,
            'response': {
                'sandbox_init_point': SANDBOX_INIT_POINT_URL,
                'init_point': INIT_POINT_URL
            }
        }
        with self.assertRaises(RedirectNeeded) as exc:
            self.provider.get_form(
                payment=self.payment)
            self.assertEqual(exc.args[0], SANDBOX_INIT_POINT_URL)
        self.assertEqual(self.payment.status, PaymentStatus.WAITING)
        self.assertEqual(self.payment.captured_amount, Decimal('0'))

    def test_process_data_returns_200_on_http_post_request(self):
        request = MagicMock()
        request.GET = {}
        response = self.provider.process_data(self.payment, request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.payment.captured_amount, Decimal('0'))
        self.assertEqual(self.payment.status, PaymentStatus.WAITING)

    @patch('mercadopago.MP.get_payment')
    def test_process_data_handles_payment_info(self, mocked_get_payment):
        request = MagicMock()
        request.GET = {'data.id': '123456', 'type': 'payment'}
        mocked_get_payment.return_value = {
            'status': 200,
            'response': {
                'status': 'approved'
            }
        }
        response = self.provider.process_data(self.payment, request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.payment.captured_amount, self.payment.total)
        self.assertEqual(self.payment.status, PaymentStatus.CONFIRMED)
        self.assertEqual(self.payment.transaction_id, '123456')
        self.assertEqual(self.payment.extra_data,
            json.dumps(mocked_get_payment.return_value))

    @patch('mercadopago.MP.get_payment')
    def test_process_data_handles_no_payment_post_requests(
        self, mocked_get_payment):
        request = MagicMock()
        request.GET = {'another_post_request': 'no_data',
            'another_data': 'other_data'}
        mocked_get_payment.return_value = {
            'status': 200,
            'response': {
                'status': 'approved'
            }
        }
        response = self.provider.process_data(self.payment, request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.payment.captured_amount, Decimal('0'))
        self.assertEqual(self.payment.status, PaymentStatus.WAITING)

    @patch('mercadopago.MP.refund_payment')
    def test_provider_refunds_payment(self, mocked_get_refund_payment):
        mocked_get_refund_payment.return_value ={
            'status': 201,
            'response': {
                'status': 'approved'
            }
        }
        self.provider.refund(self.payment)
        self.assertEqual(self.payment.captured_amount, Decimal('0'))
        self.assertEqual(self.payment.status, PaymentStatus.REFUNDED)
        self.assertEqual(self.payment.extra_data,
            json.dumps(mocked_get_refund_payment.return_value))

    @patch('mercadopago.MP.create_preference')
    def test_create_payment_return_preference(self, mocked_create_preference):
        mocked_create_preference.return_value = {
            'status': 200,
            'response':{
                'items': ['items'],
                'notification_url': 'https://yourhost.com/process_response',
                'back_urls': {
                    'success': 'https://success.com',
                    'failure': 'https://failure.com',
                    'pending': 'https://pending.com'
                }
            }
        }
        created_payment = self.provider.create_payment(self.payment)
        self.assertEqual(created_payment, mocked_create_preference.return_value)
        self.assertEqual(self.payment.extra_data,
            json.dumps(mocked_create_preference.return_value))

    def test_create_preference_data_returns_dictionary(self):
        result = self.provider.create_preference_data(self.payment)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result['back_urls']['success'],
            self.payment.get_success_url())
        self.assertEqual(result['back_urls']['failure'],
            self.payment.get_failure_url())
        self.assertEqual(result['external_reference'], self.payment.token)

    @patch('mercadopago.MP.get_payment')
    def test_get_payment_information_return_payment_details(self,
        mocked_get_payment):
        mocked_get_payment.return_value = {
            'status': 200,
            'response': {
            }
        }
        result = self.provider.get_payment_information(
            self.payment.transaction_id)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result, mocked_get_payment.return_value)

    @patch('mercadopago.MP.get_payment')
    def test_get_payment_raises_paymentError_on_404(self, mocked_get_payment):
        mocked_get_payment.return_value = {
            'status': 404,
            'response': {
                'message': 'Payment not found',
                'error': 'not found'
            }
        }
        with self.assertRaises(PaymentError) as exc:
            self.provider.get_payment_information(self.payment.transaction_id)

    @patch('mercadopago.MP.create_preference')
    def test_create_payment_raises_paymentError_on_400(
        self, mocked_create_preference):
        mocked_create_preference.return_value = {
            'status': 400,
            'response': {
                'message': 'items needed',
                'error': 'invalid items'
            }
        }
        with self.assertRaises(PaymentError) as exc:
            self.provider.create_payment(self.payment)
