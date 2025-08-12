# -*- coding: utf-8 -*-
import base64
import io
from datetime import datetime
import json
import xlsxwriter
from odoo import models
from odoo.exceptions import ValidationError
from odoo.tools import json_default


class RentalLeaseManagementReportXlsx(models.AbstractModel):
    """Model for creating xlsx Report"""
    _name = 'rental.lease.management.report.xlsx'

    def rental_report_excel(self, order_id):
        """function for getting the values"""
        docs = self.env['rental.lease.management.make.report'].browse(order_id)
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
                where_query = "WHERE " + "AND ".join(
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
            results.append({'company_id': doc.company_id.id})
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'rental.lease.management.report.xlsx',
                     'options': json.dumps(results, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Rent Lease Report',
                     },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        """generating xlsx report"""
        company_id = self.env['res.company'].search([('id', '=', data[1]['company_id'])])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        workbook.add_format(
            {'font_size': '11px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        left_align = workbook.add_format({'font_size': '10px', 'align': 'left'})
        right_align = workbook.add_format({'font_size': '10px', 'align': 'right'})
        header = workbook.add_format({'font_size': '10px', 'align': 'center', 'bold': True})
        money_format = workbook.add_format(
            {'num_format': '##0.00,#$', 'font_size': '10px', 'bold': True})
        headings = ['name', 'tenant', 'property', 'owner', 'type', 'amount', 'start_date', 'end_date', 'states']
        image_data = io.BytesIO(base64.b64decode(company_id.logo))
        sheet.insert_image("H2", "logo.png", {'image_data': image_data, 'x_scale': 0.05, 'y_scale': 0.05})
        sheet.merge_range('H5:I5', company_id.name)
        if company_id.street:
            sheet.merge_range('H6:I6', company_id.street)
        if company_id.phone:
            sheet.merge_range('H7:I7', company_id.phone)
        if company_id.email:
            sheet.merge_range('H8:I8', company_id.email)
        sheet.merge_range('A9:I10', 'RENT LEASE REPORT', head)
        date = datetime.today()
        sheet.merge_range('A12:B12', F"DATE : {date.strftime('%Y-%m-%d')}", header)
        tenants = []
        for item in data[0]:
            tenants.append(item['tenant'])
        if len(set(tenants)) == 1:
            sheet.merge_range('C12:D12', F'TENANTS : {tenants[0]}', header)
            headings.remove('tenant')
        for col, heading in enumerate(headings):
            sheet.set_column(14, col, 20)
            sheet.write(14, col, heading.upper().replace("_", " "), header)
            row = 14
            for value in data[0]:
                row += 1
                if heading in ['amount', 'start_date', 'end_date']:
                    sheet.write(row, col, value[heading], right_align)
                    if heading == 'amount':
                        sheet.write(row, col, value[heading], money_format)
                else:
                    sheet.write(row, col, value[heading], left_align)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
