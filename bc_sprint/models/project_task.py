from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = "project.task"

    sprint_id = fields.Many2one('sprint', string="Sprint")
    state_id = fields.Many2one('sprint.state', string="State from Sprint")

    @api.model
    def _group_expand_states(self, states, domain, order):
        return self.env['project.state'].search([], order='sequence').ids

