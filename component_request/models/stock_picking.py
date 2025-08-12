# -*- coding: utf-8 -*-
from odoo import models, fields


class StockPicking(models.Model):
    """stock picking class inherited from stock picking added a custom module id as aFF
    Many 2one field to connect the tables"""
    _inherit = 'stock.picking'

    component_request_id = fields.Many2one('component.request')
