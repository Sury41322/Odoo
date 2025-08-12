# -*- coding: utf-8 -*-
""" Rental / Lease management Model
app password - ajzz phfn labl iwjt """

from datetime import datetime
from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError


class RentalLeaseManagement(models.Model):
    """Rental and Lease Management Class"""
    _name = 'rental.lease.management'
    _description = 'Rental / Lease Management'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Ref No:", default="New")
    property_ids = fields.One2many(comodel_name='property.order.lines',
                                   inverse_name="property_order_id",
                                   string="Properties")
    type = fields.Selection([("Rented", "Rent"), ("Leased", "Lease")],
                            string="Property Type", default="Rented", tracking=True)
    tenant_id = fields.Many2one("res.partner", "Tenant",
                                store=True, required=True)
    start_date = fields.Date(default=datetime.now())
    end_date = fields.Date(required=True)
    duration = fields.Integer(compute="_compute_duration")
    sales_person_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    states = fields.Selection([("Draft", "Draft"), ("To_Approve", "To Approve"),
                               ("Confirmed", "Confirmed"),
                               ("Closed", "Closed"), ("Expired", "Expired")],
                              default="Draft", tracking=True, index=True)
    sub_total = fields.Float(string='Sub Total', compute='_compute_total_amount')
    invoice_ids = fields.Many2many("account.move", compute="_compute_invoice_count")
    invoice_count = fields.Integer(compute="_compute_invoice_count", string="Invoice")
    invoice_amount = fields.Float()
    payment_status = fields.Selection([('not_paid', "Pending"),
                                       ('paid', 'Paid')], default='not_paid', tracking=True)
    invoice_status = fields.Selection([('to_invoice', 'To Invoice'),
                                       ('fully_invoiced', 'Fully Invoiced')], tracking=True, default='to_invoice')

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        """Compute method for calculating the duration"""
        for record in self:
            if record.end_date:
                record.duration = (record.end_date - record.start_date).days
            else:
                record.duration = 0

    @api.depends('property_ids.total_amount')
    def _compute_total_amount(self):
        """compute method for getting the SUb total amount"""
        for record in self:
            record.sub_total = sum(record.property_ids.mapped("total_amount"))

    @api.depends('name', 'invoice_ids', 'property_ids.account_line_ids')
    def _compute_invoice_count(self):
        """compute method to get the invoice count and the invoice"""
        for record in self:
            invoices = record.property_ids.account_line_ids.move_id.filtered(lambda r: r.move_type in ('out_invoice'))
            record.invoice_ids = invoices
            record.invoice_count = len(invoices)
            self.invoice_amount = sum(invoices.mapped("amount_total_in_currency_signed"))
            amount_invoiced = sum(record.invoice_ids.mapped(lambda x: x.amount_total))
            invoice_stage = record.invoice_ids.mapped(lambda x: x.state == 'posted')
            payment_stage = record.invoice_ids.mapped(lambda x: x.payment_state == 'paid')
            if record.states == 'Confirmed':
                if all(invoice_stage) and record.sub_total == amount_invoiced:
                    # print(record.invoice_ids.mapped(lambda x: x.state == 'posted'))
                    record.write({'invoice_status': 'fully_invoiced'})
                    if all(payment_stage):
                        record.write({'payment_status': 'paid'})
                    else:
                        record.write({'payment_status': 'not_paid'})
                else:
                    record.write({'invoice_status': 'to_invoice'})

    @api.model
    def create_record(self, tenant, date, type, property):
        """function to create a record"""
        self.create({
            'tenant_id': tenant,
            'type': type,
            'end_date': date,
            'property_ids': [Command.create({
                'property_name_id': rec['property'],
                'rent_lease_amount': rec['amount'],
            }) for rec in property],
        })

    @api.model_create_multi
    def create(self, vals_list):
        """Function for Sequence"""
        for vals in vals_list:
            vals['name'] = (self.env['ir.sequence'].sudo().next_by_code('rental.lease.management') or
                            'New')
        return super().create(vals)

    def action_confirm_button(self):
        """Confirm button Action - Needed Documents"""
        attachment = self.env['ir.attachment'].search(
            [('res_model', '=', self._name),
             ('res_id', '=', self.id)])
        if not self.property_ids:
            raise ValidationError("Minimum one property needs to be added to confirm the order.")
        if not attachment:
            raise ValidationError("Please upload the documents related to this order.")
        for orders in self.property_ids:
            if self.type == "Rented":
                orders.property_name_id.rent = orders.rent_lease_amount
            else:
                orders.property_name_id.legal_amount = orders.rent_lease_amount
        is_manager = (self.env.user.has_group
                      ("property_management.group_property_management_manager"))
        if is_manager:
            self.states = "Confirmed"
            self.property_ids.property_name_id.property_state = self.type
            template = self.env.ref("property_management.mail_template_order_confirmation")
            template.send_mail(self.id, force_send=True)
            self.message_post(message_type='email_outgoing',
                              subject=template.subject,
                              body=template.body_html, )
        else:
            self.states = "To_Approve"

    def action_close_button(self):
        """Close button Action - stage(Close)"""
        self.states = "Closed"
        self.property_ids.property_name_id.property_state = "Draft"
        template = self.env.ref("property_management.mail_template_order_closing")
        template.send_mail(self.id, force_send=True)

    def action_return_button(self):
        """Return button Action - stage (Draft)"""
        self.states = "Draft"
        self.property_ids.property_name_id.property_state = "Draft"

    def action_expired_button(self):
        """Expired button Action - stage (Expired)"""
        self.states = "Expired"
        self.property_ids.property_name_id.property_state = "Draft"
        template = self.env.ref("property_management.mail_template_order_expired")
        template.send_mail(self.id, force_send=True)

    def action_to_approve(self):
        """action method for managers approval"""
        self.write({'states': 'Confirmed'})
        self.property_ids.property_name_id.property_state = self.type
        template = self.env.ref("property_management.mail_template_order_confirmation")
        template.send_mail(self.id, force_send=True)

    def _prepare_invoice(self):
        invoice_data = {
            'partner_id': self.tenant_id.id,
            'move_type': 'out_invoice',
            'invoice_date': self.start_date,
            'rent_lease_order_id': self.id,
        }
        return invoice_data

    def create_invoices(self, new_invoice):
        """Create the invoice pass the id in parameter"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': new_invoice.id
        }

    def _update_quantity(self, line):
        """update quantity of order line"""
        sum_qty = sum(line.account_line_ids.mapped('quantity'))
        return sum_qty

    def _create_invoice_line(self, line, invoice_ids):
        invoice_ids.write({
            'invoice_line_ids': [(Command.create(
                {
                    'name': line.property_name_id.name,
                    'price_unit': line.rent_lease_amount,
                    'quantity': self.duration - self._update_quantity(line),
                }))]
        })
        for inv_line in invoice_ids.invoice_line_ids:
            property_line = self.property_ids.filtered(lambda x: x.property_name_id.name == inv_line.name)
            property_line.write({'account_line_ids': [(Command.link(inv_line.id))]})

    def action_create_invoice(self):
        """Button Action to create INVOICE for the Property Order"""
        if self.invoice_ids:
            for record in self.invoice_ids:
                if record.state == 'draft':
                    for line in self.property_ids:
                        match_found = False
                        for inv_line in record.invoice_line_ids:
                            if line.property_name_id.name == inv_line.name:
                                match_found = True
                        if not match_found:
                            if line.duration - self._update_quantity(line) != 0:
                                self._create_invoice_line(line, record)
                    return self.create_invoices(record)
                else:
                    new_invoice = self.env['account.move'].create(self._prepare_invoice())
                    for line in self.property_ids:
                        if line.duration - self._update_quantity(line) != 0:
                            self._create_invoice_line(line, new_invoice)
                    return self.create_invoices(new_invoice)
        else:
            new_invoice = self.env['account.move'].create(self._prepare_invoice())
            for line in self.property_ids:
                if line.duration - self._update_quantity(line) == 0:
                    continue
                else:
                    self._create_invoice_line(line, new_invoice)
            return self.create_invoices(new_invoice)

    def action_view_invoice(self):
        """This action is for viewing the invoice_ids that are part of our
        rental_lease_management orders
        here the customer reference is been specified while creating the data by
        giving out the order name as
        the customer reference , thus will be able to filter out using the domain"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('rent_lease_order_id', '=', self.id)]
        }

    def record_expiry_checker(self):
        """scheduler which check daily if the property order has been expired or not"""
        rental = self.search([('states', '!=', 'Expired')])
        for record in rental:
            if record.end_date == datetime.today().date():
                record.states = "Expired"
                record.property_ids.property_name_id.property_state = "Draft"
                template = self.env.ref("property_management.mail_template_order_expired")
                template.send_mail(record.id, force_send=True)

    def record_payment_checker(self):
        """scheduler which check daily if the payment due date is up or not"""
        records = self.search([('states', '=', 'Confirmed'),
                               ('payment_status', '!=', 'paid')])
        for record in records:
            for line in record.invoice_ids:
                remaining_days = (line.invoice_date_due - datetime.today().date()).days
                if remaining_days < 10:
                    template = self.env.ref("property_management.mail_template_payment_alert")
                    template.send_mail(record.id, force_send=True)
