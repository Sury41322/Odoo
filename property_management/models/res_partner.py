# -*- coding: utf-8 -*-
""" Res.Partner Inherited to property Management"""
from odoo import models, fields


class ResPartner(models.Model):
    """Class used for showing Smart Button in contacts """
    _inherit = 'res.partner'

    property_ids = fields.One2many(comodel_name="property.management",
                                   inverse_name='owner_id', string="Property")
    property_count = fields.Integer(compute='_compute_property_count')

    def _compute_property_count(self):
        """Compute Function for getting the property count owned by the Res.Partner"""
        for record in self:
            properties = self.env['property.management'].search([('owner_id', '=', self.id)])
            record.property_ids = properties
            record.property_count = len(properties)

    def action_view_property(self):
        """action button for viewing the property"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property',
            'res_model': 'property.management',
            'view_mode': 'list,form',
            'domain': [('owner_id', '=', self.id)]
        }
