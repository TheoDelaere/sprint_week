from odoo import models, fields

class SprintState(models.Model):
    _name = "sprint.state"
    _description = "Sprint State"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer('Sequence', default=10, help="Used to sort the types.")
    color = fields.Integer(string="Color Index")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Each state name must be unique!')
    ]
