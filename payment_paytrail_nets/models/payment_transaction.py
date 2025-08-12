# -*- coding: utf-8 -*-

import json
import uuid
import requests

from odoo import models
from odoo.exceptions import ValidationError


class PaymentTransaction(models.Model):
    """class for payment transaction."""
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        paytrail_tx_values = dict(processing_values)
        payload = self._paytrail_form_payment_json()
        token = self._get_paytrail_url_token(payload)
        if token.get("status") == "error":
            raise ValidationError(token.get("message"))
        paytrail_tx_values[
            "paytrail_url"
        ] = f"/payment/paytrail/redirect?url={token.get('href')}"
        return paytrail_tx_values

    def _paytrail_form_payment_json(self):
        unwanted_char = self.reference.find("-")
        if unwanted_char != -1:
            ref = self.reference[:unwanted_char]
        else:
            ref = self.reference
        if self.env.company.currency_id.name != "EUR":
            from_currency = self.env['res.currency'].search([('name', '=', 'USD')])
            to_currency = self.env['res.currency'].search([('name', '=', 'EUR')])
            rate = self.env['res.currency']._get_conversion_rate(to_currency, from_currency)
        else:
            rate = 1
        order = self.env['sale.order'].search([('name', '=', ref)], limit=1)
        stamp = str(uuid.uuid4())
        reference = self.reference
        currency = "EUR"
        language = "EN"
        items = Item._get_items(Item, order, rate)
        amount = sum(list(map(lambda x: x['unitPrice'] * x['units'], items)))
        customer = Customer(self.env.user)
        redirecturls = RedirectUrls('https://efbac63a1098.ngrok-free.app/payment/paytrail/success',
                                    'https://efbac63a1098.ngrok-free.app/payment/paytrail/cancel', )
        usePricesWithoutVat = False
        b = Body(stamp, reference, amount,
                 currency, language, items, customer,
                 redirecturls, usePricesWithoutVat)
        body = json.dumps(b.toDictionary(), separators=(',', ':'))
        return body

    def _get_paytrail_url_token(self, payload):
        headers = self.provider_id._get_paytrail_header(payload)
        url = "https://services.paytrail.com/payments"
        r = requests.post(url=url, headers=headers, data=payload)
        if r.status_code == 201:
            data = r.json()
            return data
        res = r.json()
        return res

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != "paytrail" or len(tx) == 1:
            return tx
        reference = notification_data.get("checkout-reference")

        tx = self.search([('reference', '=', reference)], limit=1)
        return tx

    def _process_notification_data(self, notification_data):
        self.ensure_one()
        super()._process_notification_data(notification_data)
        self._validate_tx_form(notification_data)

    def _validate_tx_form(self, notification_data):
        status = notification_data.get("checkout-status")
        if status == 'ok':
            self._set_done()
        elif status == 'fail':
            self._set_canceled()
        else:
            self._set_pending()


class Item:
    """class to define the items in the order"""

    def _get_items(self, order, rate):
        item = []
        for product in order.order_line:
            item.append({
                'unitPrice': int(((product.price_unit + product.price_tax) * rate) * 100),
                'units': product.product_uom_qty,
                'vatPercentage': product.tax_id.amount,
                'productCode': product.product_id.name,
            })
        return item


class Customer:
    """class to define the customer datas"""

    def __init__(self, data) -> None:
        self.email = data.email


class RedirectUrls:
    """class to define redirect Urls"""

    def __init__(self, success: str, cancel: str) -> None:
        self.success = success
        self.cancel = cancel


class Body:
    """class to define Body """

    def __init__(self, stamp: str, reference: str, amount: int,
                 currency: str, language: str, items: list[Item], customer: Customer,
                 redirectUrls: RedirectUrls, usePricesWithoutVat: bool) -> None:
        self.stamp = stamp
        self.reference = reference
        self.amount = amount
        self.currency = currency
        self.language = language
        self.items = items
        self.customer = customer
        self.redirectUrls = redirectUrls
        self.usePricesWithoutVat = usePricesWithoutVat

    def toDictionary(self) -> dict:
        return dict({
            "stamp": self.stamp,
            "reference": self.reference,
            "amount": self.amount,
            "currency": self.currency,
            "language": self.language,
            "items": self.items,
            "customer": self.customer.__dict__,
            "redirectUrls": self.redirectUrls.__dict__
        })
