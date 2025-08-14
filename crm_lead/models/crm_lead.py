import datetime

from odoo import models, api, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self, period=None, factor=None):
        leads, invoice = self._get_data_according_to_period(period, factor)
        company_id = self.env.company
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        user_revenue = sum(invoice.mapped("amount_total_signed"))
        won = leads.filtered(lambda l: l.stage_id.is_won == True)
        lost = leads.search([('active', '=', False)])
        win_ratio = len(won) / (len(won) + len(lost)) if won else 0
        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'revenue': user_revenue,
            'win_ratio': win_ratio,
            'won_amount': sum(won.mapped('expected_revenue')),
            'lost_amount': sum(lost.mapped('expected_revenue')),
            'currency': currency,
        }

    def _get_data_according_to_period(self, period=None, factor=None):
        company_id = self.env.company
        # Year function
        if period == "year":
            year = datetime.date.today().year
            leads = self.search([
                ('company_id', '=', company_id.id),
                ('user_id', '=', self.env.user.id),
            ])
            invoice = self.env['account.move'].search([
                ('company_id', '=', company_id.id),
                ('invoice_user_id', '=', self.env.user.id)])
            invoice_create_date = invoice.filtered(lambda x: x.create_date.year == year)
            if factor == 'create_date':
                leads_create_date = leads.filtered(lambda x: x.create_date.year == year)
                return leads_create_date, invoice_create_date
            leads_expiry_date = leads.filtered(
                lambda x: x.date_deadline.year == year if x.date_deadline else x.date_deadline)
            return leads_expiry_date, invoice_create_date
        # Month Function
        elif period == "month":
            month = datetime.date.today().month
            leads = self.search([
                ('company_id', '=', company_id.id),
                ('user_id', '=', self.env.user.id),
            ])
            invoice = self.env['account.move'].search([
                ('company_id', '=', company_id.id),
                ('invoice_user_id', '=', self.env.user.id)])
            invoice_create_date = invoice.filtered(lambda x: x.create_date.month == month)
            if factor == 'create_date':
                leads_create_date = leads.filtered(lambda x: x.create_date.month == month)
                return leads_create_date, invoice_create_date
            leads_expiry_date = leads.filtered(
                lambda x: x.date_deadline.month == month if x.date_deadline else x.date_deadline)
            return leads_expiry_date, invoice_create_date
        # Week Function
        elif period == "week":
            week = datetime.date.today().isocalendar()[1]
            leads = self.search([
                ('company_id', '=', company_id.id),
                ('user_id', '=', self.env.user.id),
            ])
            invoice = self.env['account.move'].search([
                ('company_id', '=', company_id.id),
                ('invoice_user_id', '=', self.env.user.id)])
            invoice_create_date = invoice.filtered(lambda x: x.create_date.isocalendar()[1] == week)
            if factor == 'create_date':
                leads_create_date = leads.filtered(lambda x: x.create_date.isocalendar()[1] == week)
                return leads_create_date, invoice_create_date
            leads_expiry_date = leads.filtered(
                lambda x: x.date_deadline.isocalendar()[1] == week if x.date_deadline else x.date_deadline)
            return leads_expiry_date, invoice_create_date
        # Quarter fucntion
        elif period == "quarter":
            quarter = (datetime.date.today().month - 1) // 3 + 1
            leads = self.search([
                ('company_id', '=', company_id.id),
                ('user_id', '=', self.env.user.id),
            ])
            invoice = self.env['account.move'].search([
                ('company_id', '=', company_id.id),
                ('invoice_user_id', '=', self.env.user.id)])
            invoice_create_date = invoice.filtered(lambda x: (x.create_date.month - 1) // 3 + 1 == quarter)
            if factor == 'create_date':
                leads_create_date = leads.filtered(lambda x: (x.create_date.month - 1) // 3 + 1 == quarter)
                return leads_create_date, invoice_create_date
            leads_expiry_date = leads.filtered(
                lambda x: (x.date_deadline.month - 1) // 3 + 1 == quarter if x.date_deadline else x.date_deadline)
            return leads_expiry_date, invoice_create_date
        # Else
        leads = self.search([
            ('company_id', '=', company_id.id),
            ('user_id', '=', self.env.user.id)
        ])
        invoice = self.env['account.move'].search([('company_id', '=', company_id.id)
                                                      , ('invoice_user_id', '=', self.env.user.id)])
        return leads, invoice
