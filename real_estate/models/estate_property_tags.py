from odoo import models,fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags (Many2Many)"

    name = fields.Char()
