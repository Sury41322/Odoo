# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ComponentOrderLines(models.Model):
    """component order lines for getting the product from the product.template"""
    _name = 'component.order.lines'
    _description = "Component order Lines"
    _inherit = 'product.catalog.mixin'

    order_id = fields.Many2one('component.request')
    component_id = fields.Many2one("product.product")
    po_order_line_ids = fields.Many2many("purchase.order.line")
    request_type = fields.Selection([('purchase_order', "Purchase Order"),
                                     ('internal_transfer', "Internal Transfer")])
    seller_ids = fields.Many2many('res.partner')
    from_location_id = fields.Many2one('stock.location', domain=[('usage', '=', 'internal')])
    to_location_id = fields.Many2one('stock.location', domain=[('usage', '=', 'internal')])
    quantity = fields.Integer(default=1)
    price = fields.Float(compute="_compute_price")
    total_price = fields.Float(compute="_compute_total_price")

    @api.depends("component_id.standard_price", "component_id.lst_price")
    def _compute_price(self):
        """Compute method for calculating price if the cost price
         is 0 get the sales price"""
        for record in self:
            if record.component_id.standard_price == 0:
                record.price = record.component_id.lst_price
            else:
                record.price = record.component_id.standard_price

    @api.depends("quantity", "price")
    def _compute_total_price(self):
        """compute method to calculate the total depending
        on the quantity and price for each order lines"""
        for record in self:
            record.total_price = record.quantity * record.price
