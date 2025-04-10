from datetime import date
from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    sprint_id = fields.Many2one('sprint', string="Sprint")
    state_id = fields.Many2one('sprint.state', string="State from Sprint", group_expand='_group_expand_states')
    testing = fields.Html(string="Testing", stored=True, copied=True, help="Testing description")

    @api.model
    def _group_expand_states(self, states, domain):
        allowed_names = ['Nouveau', 'Urgent', 'Week 1', 'Week 2', 'Week 3']
        try:
            return self.env['sprint.state'].search([('name', 'in', allowed_names)])
        except Exception:
            return self.env['sprint.state'].search([])

    def compute_something(self):
        week1_state = self.env['sprint.state'].search([('name', '=', 'Week 1')])
        week2_state = self.env['sprint.state'].search([('name', '=', 'Week 2')])
        week3_state = self.env['sprint.state'].search([('name', '=', 'Week 3')])
        state_test = self.env['sprint.state'].search([('name', '=', date.today().strftime("%d-%m-%Y"))])
        if state_test.name != date.today().strftime("%d-%m-%Y"):
            new_state = self.env['sprint.state'].create({
                'name': date.today().strftime("%d-%m-%Y"),
            })
        else :
            new_state = state_test
        
        for task in self:
            if task.state_id == week1_state:
                task.state_id = new_state.id
            elif task.state_id == week2_state:
                task.state_id = week1_state.id
            elif task.state_id == week3_state:
                task.state_id = week2_state.id
            print(task.name, " = ", task.state_id.name)
        return {"success": True}