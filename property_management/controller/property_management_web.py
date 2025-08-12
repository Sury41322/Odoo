# -*- coding: utf-8 -*-
from odoo.http import request, route
from odoo import http

class PropertyManagementWeb(http.Controller):
    """Property Management Controller"""

    @http.route("/order_webform",auth='user',website=True)
    def order_webform(self):
        """Function to pass the data from model to the qweb"""
        order = http.request.env['rental.lease.management'].search([])
        tenant = request.env.user.partner_id
        state = http.request.env['res.country.state'].search([])
        country = http.request.env['res.country'].search([])
        property_ids = http.request.env['property.management'].search([
            ('property_state','=','Draft')])
        return http.request.render('property_management.create_order',{
            'order':order,
            'property':property_ids,
            'tenant':tenant,
            'country':country,
            'state':state,})

    @http.route("/my/rental_lease_order",auth='user',website=True)
    def my_rental_lease_order(self):
        """To show the orders specified to the user"""
        order = request.env['rental.lease.management'].search([
            ('tenant_id','=',request.env.user.partner_id.id)])
        return http.request.render('property_management.portal_my_rental_lease_order',
                                   {'order':order})
        # return request.render("property_management.website_rental_orders")

    @http.route("/rental_lease_order/<model(rental.lease.management):order>/",
                auth='user',website=True)
    def display_order(self,order):
        """order info according to id"""
        return request.render('property_management.portal_rent_order', {'order': order})

    @route('/order_webform/submit',type="http", auth='user',website=True)
    def request_submit(self,):
        """after submitting tenant thanks"""
        return request.render("property_management.tenant_thanks")
