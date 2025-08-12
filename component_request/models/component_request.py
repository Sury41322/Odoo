# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError


class ComponentRequest(models.Model):
    """This class defines the functions of the component request main module"""
    _name = 'component.request'
    _description = "Component Request Module"

    STATE_SELECTION = [('draft', 'DRAFT'),
                       ('submitted', 'SUBMIT'),
                       ('approved', 'APPROVE'),
                       ('done', 'DONE'),
                       ('rejected', ' REJECT'), ]

    name = fields.Char(default="New", string="Reference No")
    responsible_user_id = fields.Many2one("res.users", default=lambda self: self.env.user.id)
    order_line_ids = fields.One2many("component.order.lines", 'order_id')
    state = fields.Selection(selection=STATE_SELECTION, default='draft')
    purchase_order_count = fields.Integer(compute="_compute_purchase_order_internal_transfer")
    internal_transfer_count = fields.Integer(compute="_compute_purchase_order_internal_transfer")
    sub_total = fields.Float(compute="_compute_sub_total")

    @api.depends("order_line_ids")
    def _compute_sub_total(self):
        """compute method for getting the total amount from the order lines"""
        for record in self:
            record.sub_total = sum(record.order_line_ids.mapped('total_price'))

    def _compute_purchase_order_internal_transfer(self):
        """compute function for calculating the purchase order
        count assigning the purchase order and delivery"""
        for record in self:
            purchase_orders = self.env['purchase.order'].search([('component_request_id', "=", self.id)])
            transfer = self.env['stock.picking'].search([('component_request_id', "=", self.id)])
            record.purchase_order_count = len(purchase_orders)
            record.internal_transfer_count = len(transfer)

    @api.model_create_multi
    def create(self, vals_list):
        """function for creating sequence for the model"""
        vals = []
        for vals in vals_list:
            vals['name'] = (self.env['ir.sequence'].next_by_code('component.request') or 'New')
        if vals['order_line_ids'] == []:
            raise ValidationError("""Please dd at least 1 Order
             - OrderLine cannot be empty""")
        return super().create(vals)

    def action_submit_button(self):
        """button action to submit the component request"""
        if self.order_line_ids:
            self.write({'state': 'submitted'})
        else:
            raise ValidationError("Please add at least one Order line")

    def action_approve_button(self):
        """approve action button"""
        self.write({'state': 'approved'})

    def action_deny_button(self):
        """button action for denying the request"""
        self.write({'state': 'rejected'})

    def action_reject_button(self):
        """button for Req Head to Reject the request"""
        self.write({'state': 'rejected'})

    def _prepare_po(self, seller):
        """function used to create the purchase order"""
        return {
            'component_request_id': self.id,
            'partner_id': seller.id,
            'user_id': self.responsible_user_id.id,
        }

    def _rfq_lines(self, record, rfq):
        """function for creating the rfq lines"""
        rfq.write({
            'order_line': [(Command.create({
                'product_id': record.component_id.id,
                'price_unit': record.price,
                'product_qty': record.quantity,
            }))]
        }
        )
        for order_lines in rfq.order_line:
            component_line = (self.order_line_ids.filtered
                              (lambda x: x.component_id == order_lines.product_id))
            component_line.write({'po_order_line_ids': [(Command.link(order_lines.id))]})

    def _prepare_internal_transfer_order(self):
        """function for creating the internal transfer"""
        delivery = {
            'component_request_id': self.id,
            'user_id': self.responsible_user_id.id,
            'picking_type_id': 7,
        }
        return delivery

    def _internal_transfer_order_lines(self, internal_transfer, line):
        """function to write internal transfer order line"""
        internal_transfer.write({
            'location_id': line.from_location_id,
            'location_dest_id': line.to_location_id,
            'move_ids': [(Command.create({
                'product_id': line.component_id.id,
                'product_uom_qty': line.quantity,
                'name': line.component_id.name
            }))]
        })

    def action_create_rfq_button(self, ):
        """Button action of creating the rfq"""
        purchase_orders = (self.order_line_ids.filtered
                           (lambda x: x.request_type == 'purchase_order'))
        internal_orders = (self.order_line_ids.filtered
                           (lambda x: x.request_type == 'internal_transfer'))
        sellers = self.order_line_ids.mapped('seller_ids')
        if purchase_orders:
            for seller in sellers:
                order_with_seller = purchase_orders.filtered(lambda x: seller in x.seller_ids)
                new_rfq = self.env['purchase.order'].create(self._prepare_po(seller))
                for order in order_with_seller:
                    self._rfq_lines(order, new_rfq)
        if internal_orders:
            routes = internal_orders.grouped(lambda x: x.from_location_id and x.to_location_id)
            print(routes)
            for route in routes:
                internal_transfer = (self.env['stock.picking'].create
                                     (self._prepare_internal_transfer_order()))
                for order in routes[route]:
                    self._internal_transfer_order_lines(internal_transfer, order)
                internal_transfer.action_confirm()
        self.write({'state': 'done'})

    def action_view_purchase_order(self):
        """function for viewing the purchase order with domain in smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFQ',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('component_request_id', '=', self.id)]
        }

    def action_view_internal_transfer(self):
        """function for viewing the internal transfer from smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfer',
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('component_request_id', '=', self.id)]
        }
