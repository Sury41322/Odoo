# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteProduct(http.Controller):
    @http.route('/get_latest_property', auth="public", type='json',
                website=True)
    def get_latest_property(self):
        """Get Lastest Property."""
        latest_property = request.env[
            'property.management'].sudo().search_read([], fields=['name', 'id', 'property_image'], order='id desc')
        values = {
            'property': latest_property,
        }
        return values

    @http.route("/property/<model(property.management):property_id>", type='http', auth='public', website=True)
    def get_details(self, property_id):
        result = request.env['property.management'].search([('id', '=', property_id.id)])
        return request.render("property_management.property_details", {'property': result})
