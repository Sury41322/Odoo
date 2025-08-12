
from odoo import  fields, models

class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection=[('paytrial', "paytrial")])
    paytrial_merchant_key = fields.Char(
        string="Merchant ID",
        help="The key solely used to identify the Merchant with paytrial",
    )
    paytrial_secret_key = fields.Char(
        string="Secret Key",
    )

    # def _compute_feature_support_fields(self):
    #     """ Override of `payment` to enable additional features. """
    #     super()._compute_feature_support_fields()
    #     self.filtered(lambda p: p.code == 'paytrial').update({
    #         'support_express_checkout': True,
    #         'support_manual_capture': 'partial',
    #         'support_refund': 'partial',
    #         'support_tokenization': True,
    #     })
    #
    # def _paytrial_has_connected_account(self):
    #     self.ensure_one()
    #     return False
    #
    # def _paytrial_onboarding_us_ongoing(self):
    #     self.ensure_one()
    #     return False
    #
    # def action_paytrial_connect_account(self,menu_id=None):
    #     self.ensure_one()
    #     if self.state == 'enabled':
    #         self.env['onboarding.orboarding.step'].action_validate_step_payment_provider()
    #         action = { 'type' : 'ir.actions.act_window_close'}
    #     else:
    #         connected_account = self._paytrial_fetch_or_create_aconnected_account()
    #
    #         if not menu_id:
    #             menu = self.env.ref("account_payment.payment_provider_menu",False)
    #             menu_id = menu and menu.id
    #
    #         account_link_url = self._paytrila_create_account_link(connected_account['id'],menu_id)
    #         if account_link_url:
    #             action = {
    #                 'type': 'ir.actions.act_url',
    #                 'url': account_link_url,
    #                 'target' : 'self'
    #             }
    #         else:
    #             action = {
    #                 'type': 'ir.actions.act_window',
    #                 'model': 'payment.provider',
    #                 'views': [[False, 'form']],
    #                 'res_id': self.id,
    #             }
    #     return action
# class PaymentProvider(models.Model):
#     _inherit = 'payment.provider'
#
#     code = fields.Selection(selection_add=[('paytrial', 'Paytrial')], ondelete={'paytrial': 'set default'})
#
#     #=== COMPUTE METHODS ===#
#
#     def _compute_feature_support_fields(self):
#         """ Override of `payment` to enable additional features. """
#         super()._compute_feature_support_fields()
#         self.filtered(lambda p: p.code == 'paytrial').update({
#             'support_express_checkout': True,
#             'support_manual_capture': 'partial',
#             'support_refund': 'partial',
#             'support_tokenization': True,
#         })
#
#     # === CONSTRAINT METHODS ===#
#
#     @api.constrains('state', 'code')
#     def _check_provider_state(self):
#         if self.filtered(lambda p: p.code == 'paytrial' and p.state not in ('test', 'disabled')):
#             raise UserError(_("paytrial providers should never be enabled."))
#
#     def _get_default_payment_method_codes(self):
#         """ Override of `payment` to return the default payment method codes. """
#         default_codes = super()._get_default_payment_method_codes()
#         if self.code != 'paytrial':
#             return default_codes
#         return const.DEFAULT_PAYMENT_METHOD_CODES
