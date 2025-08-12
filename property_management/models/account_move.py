"""Module for Account Move"""
from odoo import models,fields

class AccountMove(models.Model):
    """Property Management Inherits Account Move"""
    _inherit = 'account.move'

    rent_lease_order_id = fields.Many2one('rental.lease.management',string="Order")
