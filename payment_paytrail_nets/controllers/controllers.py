# -*- coding: utf-8 -*-

from odoo import http
import werkzeug

from odoo.http import request


class PaytrailController(http.Controller):

    @http.route(["/payment/paytrail/redirect"], type="http", auth="public", csrf=False, )
    def paytrail_redirect(self, url, **kwargs):
        return werkzeug.utils.redirect(url)

    @http.route(['/payment/paytrail/success', '/payment/paytrail/cancel'], type='http', methods=['GET'], auth='public')
    def paytrail_get_data(self, **data):
        tx = request.env['payment.transaction']._get_tx_from_notification_data("paytrail", data)
        tx.sudo()._handle_notification_data('paytrail', data)
        return request.redirect("/payment/status")
