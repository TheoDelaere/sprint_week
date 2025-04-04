from odoo import models, fields

class SprintWeek(models.Model):
    _name = "sprint.week"
    _description = "Sprint Week"

    name = fields.Char(string="Name", required=True)
    sprint_id = fields.Many2one('sprint', string="Sprint", readonly=True)
    state_id = fields.Many2one("sprint.state", string="State")
    task_ids = fields.One2many('project.task', 'sprint_id', string="Sprint Tasks")