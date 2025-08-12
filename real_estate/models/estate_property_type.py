from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    category = fields.Integer(string="Category")
    name = fields.Char(string="Property Type" , required=True)

