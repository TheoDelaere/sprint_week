from odoo import models, fields

class Project(models.Model):
    _inherit = "project.project"

    release_ids = fields.Many2many('sprint.release', string="Sprint Release")
    release_note_ids = fields.One2many('release.note', 'project_id', string="Release Note")