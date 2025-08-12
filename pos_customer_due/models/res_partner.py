# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    """Res partner Inherited to show due limit"""
    _inherit = 'res.partner'
    credit_allowed = fields.Boolean(string="Credits Allowed")
    pos_due_limit = fields.Float(string="Limit", default=500.00)

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ['pos_due_limit']
        return result

    @api.model
    def get_remaining_amount(self, partner_id):
        """function to check whether credits are allowed"""
        record = self.search([('id', '=', partner_id)])
        if (record.credit_allowed is True):
            return record.pos_due_limit
        return False

    @api.model
    def update_remaining_due(self, partner_id, pos_due_limit):
        """function to update the limit"""
        record = self.search([('id', '=', partner_id)])
        record.pos_due_limit -= pos_due_limit
        return record.pos_due_limit
