from datetime import date
from odoo import models, fields, api, _
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    NUMBER_OF_SPRINTS_COLUMNS = 3

    sprint_id = fields.Many2one('sprint', string="Sprint", group_expand='_group_expand_sprints', default=lambda self: self.env['sprint'].search([('column_type', '=', 'new')], limit=1))
    testing = fields.Html(string="Testing", stored=True, copied=True, help="Testing description")

    def generate_next_n_sprints(self, n):
        # Try to create a sprint for this week and for the next 2 weeks
        today = date.today()
        for i in range(n):
            sprint_date = today + timedelta(days=(i * 7) - today.weekday())
            sprint_year = sprint_date.year
            sprint_week = sprint_date.isocalendar()[1]
            existing_sprint = self.env['sprint'].search([
                '&',
                ('year', '=', sprint_year),
                ('week', '=', sprint_week),
            ], limit=1)
            if not existing_sprint:
                self.env['sprint'].create({
                    'start_date': sprint_date,
                    'name': f"{sprint_year} Week {str(sprint_week).zfill(2)} sprint",
                })
            print(f"Created sprint for {sprint_date} with name {sprint_year} Week {str(sprint_week).zfill(2)} sprint")

    @api.model
    def _group_expand_sprints(self, sprints, domain):
        try:
            time_limit = date.today() + timedelta(days=self.NUMBER_OF_SPRINTS_COLUMNS * 7)
            return self.env['sprint'].search([
                "|", 
                "&", 
                ("end_date", ">", date.today()),
                ("start_date", "<=", time_limit),
                ("column_type", "!=", "sprint"),
                ("archived", "=", False)
            ], order='sequence asc, start_date asc')
        except Exception:
            return self.env['sprint'].search([])

    def compute_something(self):
        # week1_sprint = self.env['sprint'].search([('name', '=', 'Week 1')])
        # week2_sprint = self.env['sprint'].search([('name', '=', 'Week 2')])
        # week3_sprint = self.env['sprint'].search([('name', '=', 'Week 3')])
        # sprint_test = self.env['sprint'].search([('name', '=', date.today().strftime("%d-%m-%Y"))])
        # if sprint_test.name != date.today().strftime("%d-%m-%Y"):
        #     new_sprint = self.env['sprint'].create({
        #         'name': date.today().strftime("%d-%m-%Y"),
        #     })
        # else :
        #     new_sprint = sprint_test
        # for task in self:
        #     if task.sprint_id == week1_sprint:
        #         task.sprint_id = new_sprint.id
        #     elif task.sprint_id == week2_sprint:
        #         task.sprint_id = week1_sprint.id
        #     elif task.sprint_id == week3_sprint:
        #         task.sprint_id = week2_sprint.id
        #     print(task.name, " = ", task.sprint_id.name)
        return {"success": True}
        