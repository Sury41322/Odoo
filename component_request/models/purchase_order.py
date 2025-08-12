# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrder(models.Model):
    """class doc string for purchase order"""
    _inherit = 'purchase.order'

    component_request_id = fields.Many2one('component.request', string='Component Request')
