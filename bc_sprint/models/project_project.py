from odoo import models, fields

class Project(models.Model):
    _inherit = "project.project"

    release_ids = fields.One2many('sprint.release', 'project_id', string="Sprint Release")