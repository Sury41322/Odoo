from odoo import models,fields

class Example(models.Model):
    _name = 'example.example'
    _description = "Example description"

    name = fields.Char()
    example_tags_ids = fields.Many2many('example_tags')