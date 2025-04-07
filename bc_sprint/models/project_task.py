from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    sprint_id = fields.Many2one('sprint', string="Sprint")
    state_id = fields.Many2one('sprint.state', string="State from Sprint", group_expand='_group_expand_states')

    @api.model
    def _group_expand_states(self, states, domain):
        try:
            return self.env['sprint.state'].search(domain=domain)
        except Exception:
            return self.env['sprint.state'].search([])