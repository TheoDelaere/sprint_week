from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    sprint_id = fields.Many2one('sprint', string="Sprint")
    state_id = fields.Many2one('sprint.state', string="State from Sprint", group_expand='_group_expand_states')
    testing = fields.Html(string="Testing", stored=True, copied=True, help="Testing description")

    @api.model
    def _group_expand_states(self, states, domain):
        try:
            return self.env['sprint.state'].search(domain=domain)
        except Exception:
            return self.env['sprint.state'].search([])

    def compute_something(self):
        week1_state = self.env['sprint.state'].search([('name', '=', 'Week 1')])
        week2_state = self.env['sprint.state'].search([('name', '=', 'Week 2')])
        week3_state = self.env['sprint.state'].search([('name', '=', 'Week 3')])
        
        for task in self:
            if task.state_id == week3_state:
                task.state_id = week2_state.id
            if task.state_id == week2_state.id:
                task.state_id = week1_state.id
            print(task.name, " = ", task.state_id.name)
        return {"success": True}