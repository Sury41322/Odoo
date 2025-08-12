# -*- coding: utf-8 -*-
""" Property management Model"""

from odoo import models, fields, api
from odoo.exceptions import UserError

class PropertyManagement(models.Model):
    """Property Management Class"""
    _name = "property.management"
    _description = "Property Management Details"
    _inherit = ["mail.thread", 'mail.activity.mixin']

    name = fields.Char(required=True , ondelete='cascade')
    facilities = fields.Many2many('property.tags')
    property_image = fields.Image()
    address = fields.Text()
    zip_code = fields.Char()
    country_id = fields.Many2one("res.country", string="Country")
    state_id = fields.Many2one("res.country.state", "State",
                               domain="[('country_id','=',country_id)]", )
    city = fields.Char()
    owner_id = fields.Many2one("res.partner", store=True)
    can_be_sold = fields.Boolean(string="Can Be Sold")
    built_date = fields.Date(string="Built Date")
    legal_amount = fields.Float(string="Legal Amount", required=True)
    rent = fields.Float(string="Rent", required=True)
    property_state = fields.Selection(
        [("Draft", "Draft"), ("Rented", "Rented"), ("Leased", "Leased"), ("Sold", "Sold")],
        "Property State", tracking=True, default="Draft",index=True)
    description = fields.Text()
    rent_lease_count = fields.Integer(compute='_compute_rent_lease_count')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company',default=lambda self: self.env.company)

    def _compute_rent_lease_count(self):
        """Function for computing the count of rent or leased property"""
        for record in self:
            rent_lease = (self.env['rental.lease.management'].search_count(
                [('property_ids.property_name_id', '=', self.id)]))
            record.rent_lease_count = rent_lease

    def unlink(self):
        """unlink method where if the order has only one property
         delete that property too"""
        for record in self:
            if record.property_state != "Draft":
                raise UserError("Cannot Delete a property which is SOLD/RENTED/LEASED")
            order = self.env['property.order.lines'].search(
                [('property_name_id', '=', record.name)])
            if len(order.property_order_id.property_ids) == 1:
                order.property_order_id.unlink()
        return super().unlink()

    def action_rent_lease_count(self):
        """Button Action"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent / Lease',
            'res_model': 'rental.lease.management',
            'view_mode': 'list,form',
            'domain': [('property_ids.property_name_id', '=', self.name)],
            'context': "{'create':False}"
        }

    @api.model
    def get_values(self, property_id, type):
        record = self.browse(property_id)
        if type == 'Rented':
            return [record.owner_id.name, record.rent]
        return [record.owner_id.name, record.legal_amount]

    @api.model
    def get_latest_property(self):
        result = self.search([],order='id desc',limit=4)
        return result

class PropertyTags(models.Model):
    """Model for Property Tags"""
    _name = 'property.tags'
    _description = 'Property Tags'

    name = fields.Char(string='Facilities')
