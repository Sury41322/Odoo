# -*- coding: utf-8 -*-
"""property order line models"""
from odoo import models, fields, api


class PropertyOrderLines(models.Model):
    """Property Order Lines Model"""
    _name = 'property.order.lines'
    _description = "Property Order Lines"

    property_name_id = fields.Many2one('property.management',
                                       domain="[('property_state','=','Draft')]",
                                       ondelete="cascade")
    property_order_id = fields.Many2one('rental.lease.management',ondelete='cascade')
    rent_lease_amount = fields.Float(compute="_compute_rent_lease_amount",
                                     string="Amount", store=True, readonly=False)
    duration = fields.Integer(compute='_compute_duration')
    total_amount = fields.Integer(compute='_compute_total_amount')
    account_line_ids= fields.Many2many("account.move.line",store=True)

    @api.depends('property_name_id.rent','property_name_id.legal_amount','property_order_id.type')
    def _compute_rent_lease_amount(self):
        """Compute for getting rent or lease amount"""
        for record in self:
            if record.property_order_id.type == "Rented":
                record.rent_lease_amount = record.property_name_id.rent
            else:
                record.rent_lease_amount = record.property_name_id.legal_amount

    @api.depends('property_order_id.end_date', 'property_order_id.start_date')
    def _compute_duration(self):
        """compute method for getting the duration from start and end date"""
        for record in self:
            if record.property_order_id.end_date:
                record.duration = (
                    (record.property_order_id.end_date - record.property_order_id.start_date).days)
            else:
                record.duration = 0

    @api.depends('rent_lease_amount')
    def _compute_total_amount(self):
        """compute method for getting the total amount line by line"""
        for record in self:
            record.total_amount = record.duration * record.rent_lease_amount
