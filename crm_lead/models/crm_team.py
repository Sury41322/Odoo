from odoo import models, fields


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    crm_lead_states = fields.Many2one('crm.stage', string="Lead Stage")