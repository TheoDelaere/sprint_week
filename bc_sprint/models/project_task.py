from datetime import date
from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    sprint_id = fields.Many2one('sprint', string="Sprint", group_expand='_group_expand_sprints')
    testing = fields.Html(string="Testing", stored=True, copied=True, help="Testing description")

    @api.model
    def _group_expand_sprints(self, sprints, domain):
        allowed_names = ['Nouveau', 'Urgent', 'Week 1', 'Week 2', 'Week 3']
        try:
            return self.env['sprint'].search([('name', 'in', allowed_names)])
        except Exception:
            return self.env['sprint'].search([])

    def compute_something(self):
        week1_sprint = self.env['sprint'].search([('name', '=', 'Week 1')])
        week2_sprint = self.env['sprint'].search([('name', '=', 'Week 2')])
        week3_sprint = self.env['sprint'].search([('name', '=', 'Week 3')])
        sprint_test = self.env['sprint'].search([('name', '=', date.today().strftime("%d-%m-%Y"))])
        if sprint_test.name != date.today().strftime("%d-%m-%Y"):
            new_sprint = self.env['sprint'].create({
                'name': date.today().strftime("%d-%m-%Y"),
            })
        else :
            new_sprint = sprint_test
        
        for task in self:
            if task.sprint_id == week1_sprint:
                task.sprint_id = new_sprint.id
            elif task.sprint_id == week2_sprint:
                task.sprint_id = week1_sprint.id
            elif task.sprint_id == week3_sprint:
                task.sprint_id = week2_sprint.id
            print(task.name, " = ", task.sprint_id.name)
        return {"success": True}