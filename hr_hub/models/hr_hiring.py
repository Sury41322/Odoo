# -*- coding: utf-8 -*-
from odoo import fields, models, api


class HrHiring(models.Model):
    _name = 'hr.hiring'
    _description = 'New Hiring'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Name', required=True, )
    email = fields.Char('Personal Email', required=True, )
    phone = fields.Char('Personal Number', required=True, )
    country_id = fields.Many2one('res.country', string='Nationality', required=True, )
    department_id = fields.Many2one('hr.department', string='Department', required=True, )
    job_id = fields.Many2one('hr.job', string='Job Position', required=True, )
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    wage = fields.Monetary('Wage', required=True, )
    housing_allowance = fields.Monetary('Housing Allowance', required=True, )
    transportation_allowance = fields.Monetary('Transportations Allowance', required=True)
    other_allowances = fields.Monetary('Other Allowance', required=True)
    state = fields.Selection(
        [('draft', 'New'), ('hr_review', 'HR Review'),
         ('done', 'Approved')], string='Status', default='draft', required=True, )
    check_readonly = fields.Boolean('Check Readonly', compute='_compute_check_readonly')

    @api.depends('state')
    def _compute_check_readonly(self):
        for rec in self:
            rec.check_readonly = rec.state != 'draft'

    def action_review(self):
        fld = self.env['res.config.settings'].search([])
        for record in fld.hr_hiring_reviewer_ids:
            print(record.name)

            # self.env['mail.activity'].create({
            #     'summary': 'Approval Request',
            #     'date_deadline': fields.Date.today(),
            #     # 'user_id': record.name,
            #     'activity_type_id': 2,
            #     'res_model_id': self.env['ir.model']._get_id('res.partner'),
            #     'res_id': self.id,
            #     'user_id': record.id,
            # })
        self.state = 'hr_review'

    def action_review_approve(self):
        self.state = 'done'
