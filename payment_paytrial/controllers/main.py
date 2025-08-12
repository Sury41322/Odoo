# -*- coding: utf-8 -*-
from odoo import http


# class PaytrialController(http.Controller):
#     @http.route('/payment/paytrial/redirect', auth='public', type='http', website=True)
#     def paytrial_redirect(self, **kwargs):
#         rec = http.request.env['payment.transaction'].sudo().search([('reference','=',kwargs.get('reference'))],limit=1)
#         provider = rec.provider_id
#         values = {
#             'action_url' : provider.paytrial_base_url,
#             'merchant_id' : provider.paytrial_merchant_id,
#             'amount' : int(provider.amount),
#             'reference' : provider.reference,
#             # 'signature' : provider.paytrial_base_url
#         }
#         print(rec)
#         return http.request.render('payment_paytrial.paytrial_redirect_form',values)

class PaymentPaytrialController(http.Controller):
    _simulation_url = '/payment/paytrial/simulate_payment'

    @http.route(_simulation_url, type='json', auth='public')
    def paytrial_simulate_payment(self, **paytrial):
        """ Simulate the response of a payment request.

        :param dict data: The simulated notification data.
        :return: None
        """
        http.request.env['payment.transaction'].sudo()._handle_notification_data('paytrial', paytrial)
