from odoo import models, fields

class Sprint(models.Model):
    _name = "sprint"
    _description = "Sprint"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer('Sequence', default=10, help="Used to sort the types.")
    color = fields.Integer(string="Color Index")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Each Sprint name must be unique!')
    ]
