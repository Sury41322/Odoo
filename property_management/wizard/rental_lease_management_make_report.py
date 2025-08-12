# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields


class RentalLeaseManagementMakeReport(models.TransientModel):
    """Wizard for rental lease management """
    _name = "rental.lease.management.make.report"
    _transient_max_hours = 1

    RENT_LEASE_STATE = [("Draft", "Draft"), ("To_Approve", "To Approve"),
                        ("Confirmed", "Confirmed"),
                        ("Closed", "Closed"), ("Expired", "Expired")]

    RECORD_TYPE = [("Rented", "Rent"), ("Leased", "Lease")]
    from_date = fields.Date()
    to_date = fields.Date()
    state = fields.Selection(selection=RENT_LEASE_STATE)
    tenant_ids = fields.Many2many('res.partner')
    owner_ids = fields.Many2many('res.partner', relation="rental_lease_management_make_report_res_partner_owner_rel")
    type = fields.Selection(selection=RECORD_TYPE)
    property_ids = fields.Many2many('property.management')
    create_date = fields.Date(default=datetime.today())
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    def _is_property(self):
        for record in self:
            if len(record.property_ids.ids) > 1:
                result = []
                for items in record.property_ids.ids:
                    result.append(items)
                return (f"property_management.id IN {tuple(result)}")
            return (f"property_management.id = {record.property_ids.id}")

    def _is_tenant(self):
        for record in self:
            if len(record.tenant_ids.ids) > 1:
                tenants = []
                for tenant in record.tenant_ids.ids:
                    tenants.append(tenant)
                return (f"res_partner.id IN {tuple(tenants)}")
            return (f"res_partner.id = {record.tenant_ids.id}")

    def _is_owner(self):
        for record in self:
            if len(record.owner_ids.ids) > 1:
                owners = []
                for owner in record.tenant_ids.ids:
                    owners.append(owner)
                return (f"property_management.owner_id in {tuple(owners)}")
            return (f"property_management.owner_id = {record.owner_ids.id}")

    def action_print_pdf(self):
        """function for calling report_action for creating pdf"""
        return (self.env.ref('property_management.action_report_rental_lease_management').report_action(docids=self))

    def action_print_xlsx(self):
        """fucntion for calling rental_report_excel for creating excel"""
        return (self.env['rental.lease.management.report.xlsx'].rental_report_excel(self.id))
