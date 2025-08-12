# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rating = fields.Selection([('0', '0'),
                               ('1', '1'),
                               ('2', '2'),
                               ('3', '3'),
                               ('4', '4'),
                               ('5', '5')], default="0", string="Rating")
