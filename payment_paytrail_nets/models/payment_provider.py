# -*- coding: utf-8 -*-
import hashlib
import hmac
from odoo import models, fields, api
from odoo.exceptions import UserError


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection=[('paytrail', "Paytrail")], ondelete={'paytrail': 'set default'},

    )
    paytrail_merchant_id = fields.Char(
        string="Merchant ID",
        help="The code of the merchant account to use with this provider.",
        required_if_provider='paytrail'
    )
    paytrail_secret_key = fields.Char(
        string="Secret Key",
        help="The access code associated with the merchant account.",
        required_if_provider='paytrail'
    )

    @api.constrains('state', 'code')
    def _check_provider_state(self):
        if self.filtered(lambda p: p.code == 'paytrail' and p.state not in ('test', 'disabled')):
            raise UserError("Demo providers should never be enabled.")

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'demo').update({
            'support_express_checkout': False,
            'support_manual_capture': 'partial',
            'support_refund': 'partial',
            'support_tokenization': False,
        })

    def _get_paytrail_header(self, payload):
        headers = {
            "checkout-account": self.paytrail_merchant_id,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": '564635208570151',
            "checkout-timestamp": fields.datetime.now().isoformat(),
            "content-type": 'application/json; charset=utf-8',
        }
        enc_data = Crypto.calculate_hmac(Crypto,
                                         self.paytrail_secret_key, header=headers,
                                         body=payload)
        headers['signature'] = enc_data
        return headers


class Crypto:
    """Class for encrypting the transaction."""

    @staticmethod
    def compute_sha256_hash(message: str, secret: str) -> str:
        """funtion to compute sha256_hash"""
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()

    @staticmethod
    def calculate_hmac(self, secret: str, header: dict, body: str = '') -> str:
        """function to compute hmac"""
        data = []
        for key, value in header.items():
            if key.startswith('checkout-'):
                data.append(f'{key}:{value}')
        data.append(body)
        return self.compute_sha256_hash('\n'.join(data), secret)
