# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import ValidationError


class RentalLeaseManagementReport(models.AbstractModel):
    """Abstract Model for preparing report"""
    _name = 'report.property_management.report_rental_lease_management'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['rental.lease.management.make.report'].browse(docids)
        for doc in docs:
            where_conditions = []
            where_conditions.append(f"rental_lease_management.company_id = {doc.company_id.id} ")
            if doc.from_date:
                where_conditions.append(f"rental_lease_management.start_date >='{doc.from_date}'")
            if doc.to_date:
                where_conditions.append(f"rental_lease_management.end_date <='{doc.to_date}'")
            if doc.state:
                where_conditions.append(f"rental_lease_management.states = '{doc.state}'")

            if doc.type:
                where_conditions.append(f"rental_lease_management.type = '{doc.type}'")
            if doc.property_ids:
                where_conditions.append(doc._is_property())
            if doc.tenant_ids:
                where_conditions.append(doc._is_tenant())
            if doc.owner_ids:
                where_conditions.append(doc._is_owner())

            if where_conditions:
                where_query = f"WHERE " + "AND ".join(
                    where_conditions)
            else:
                where_query = f"WHERE rental_lease_management.company_id = {doc.company_id.id} "
            results = []
            self.env.cr.execute(f"""
                SELECT
                res_partner.name as tenant,
                (select res_partner.name from res_partner 
                    WHERE property_management.owner_id = res_partner.id) as owner,
                rental_lease_management.name as name,
                property_management.name as property,
                rental_lease_management.type as type,
                rental_lease_management.start_date as start_date,
                rental_lease_management.end_date as end_date,
                property_order_lines.rent_lease_amount as amount,
                states
                FROM rental_lease_management
                JOIN property_order_lines on property_order_lines.property_order_id = rental_lease_management.id
                JOIN property_management
                    ON property_management.id = property_order_lines.property_name_id
                JOIN res_partner
                    ON res_partner.id = rental_lease_management.tenant_id
                 {where_query}""")
            results.append(self.env.cr.dictfetchall())
        if results == [[]]:
            raise ValidationError("No record found")
        return {
            'doc_ids': docids,
            'doc_model': 'rental.lease.management.make.report',
            'docs': docs,
            'record': results
        }
