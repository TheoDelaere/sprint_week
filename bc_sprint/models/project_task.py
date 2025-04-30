from datetime import date
from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    NUMBER_OF_SPRINTS_COLUMNS = 3

    sprint_id = fields.Many2one('sprint', string="Sprint", group_expand='_group_expand_sprints', default=lambda self: self.env['sprint'].search([('name', '=', 'New')], limit=1))
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

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)

        # Identifier les sprints nécessaires
        sprint_urgent = self.env['sprint'].search([('name', '=', 'Urgent')], limit=1)
        sprint_new = self.env['sprint'].search([('name', '=', 'New')], limit=1)

        if not sprint_urgent or not sprint_new:
            raise UserError(_("Please ensure the sprints 'Urgent' and 'New' exist."))

        for task in self:
            # Priorité High (1) & Sprint = New -> Urgent
            if task.priority == '1' and (task.sprint_id == sprint_new or not task.sprint_id):
                super(ProjectTask, task).write({'sprint_id': sprint_urgent.id})

            # Priorité Low (0) & (Sprint = Urgent ou vide) -> New
            elif task.priority == '0' and (not task.sprint_id or task.sprint_id == sprint_urgent):
                super(ProjectTask, task).write({'sprint_id': sprint_new.id})
        return res

    @api.model
    def _group_expand_sprints(self, sprints, domain):
        self.generate_next_n_sprints(self.NUMBER_OF_SPRINTS_COLUMNS)
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
        