from odoo import models, fields


class Student(models.Model):
    _name = "student.student"
    _description = "Student_Description"

    name = fields.Char(string = "name")