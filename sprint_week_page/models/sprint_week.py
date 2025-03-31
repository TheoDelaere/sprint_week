from odoo import models, fields, api, _


class SprintWeek(models.Model):
    _name = 'sprint.week'
    _description = 'Sprint week model'

    name = fields.Char(string='Name', required=True)
    task_ids = fields.Many2many("project.task", string="Tasks", copy=True)
    project_id = fields.Many2one("project.project", string="Project")