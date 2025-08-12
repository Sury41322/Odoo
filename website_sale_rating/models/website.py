# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Website(models.Model):
    _inherit = 'website'

    shop_default_sort = fields.Selection(
        selection='_get_product_sort_mapping', required=True, default='website_sequence asc')

    @api.model
    def _get_product_sort_mapping(self):
        val=super()._get_product_sort_mapping()
        val.append(('rating desc', 'Rating'))
        return val