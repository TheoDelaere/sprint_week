from odoo import models, fields

class SprintWeek(models.Model):
    _name = "sprint.week"
    _descritption = "Sprint Week"

    name = fields.Char(string="Name", required=True)
    sprint_id = fields.Many2one('sprint', string="Sprint")