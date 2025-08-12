# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductProduct(models.Model):
    """Product to add custom fields """
    _inherit = 'product.product'

    pos_rating = fields.Selection([('0','0'),
           ('1', '1'),
           ('2', '2'),
           ('3', '3'),
           ('4', '4'),
           ('5', '5')], default="0", string="Rating")

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['pos_rating']
        return data

class ProductTemplate(models.Model):
    """ProductTemplate to add custom fields """
    _inherit = 'product.template'

    pos_rating = fields.Selection([('0','0'),
        ('1', '1'),
       ('2', '2'),
       ('3', '3'),
       ('4', '4'),
       ('5', '5')], string="Rating",compute="compute_price", inverse="inverse_compute_price" )

    @api.depends_context('product_variant_ids.pos_rating')
    def compute_price(self):
        """if the price is already set from while creating the product"""
        for record in self:
            if (self.product_variant_ids.pos_rating):
                record.pos_rating = self.product_variant_ids.pos_rating
            else:
                record.pos_rating = "0"

    def inverse_compute_price(self):
        """if rating is changed from template"""
        for record in self:
            self.product_variant_ids.pos_rating = record.pos_rating
