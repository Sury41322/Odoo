# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPaymentMethod(models.Model):
    """Pos Payment Method Inherited to add ledger option"""
    _inherit = 'pos.payment.method'

    is_ledger = fields.Boolean(string='Credit', help="Is a Credit Payment Method")

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ['is_ledger']
        return result
