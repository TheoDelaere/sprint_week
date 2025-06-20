from datetime import date
from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command


class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "name desc"

    NUMBER_OF_SPRINTS_COLUMNS = 3

    documentation = fields.Html(string="Documentation", store=True, copy=True, help="Documentation description")
    testing = fields.Html(string="Testing", store=True, copy=True, help="Testing description")

    sprint_id = fields.Many2one('sprint', string="Sprint", group_expand='_group_expand_sprints', default=lambda self: self.env['sprint'].search([('name', '=', 'New')], limit=1))
    release_ids = fields.Many2many('sprint.release', string="Release")
    release_note_ids = fields.Many2many('release.note', string="Release Note")

    assigned_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned User",
        help="User assigned to this task.",
        compute="_compute_assigned_user_id",
        inverse="_inverse_assigned_user_id",
        store=True
    )

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
        if vals.get("release_note_ids"):
            if self.release_note_ids:
                new_release = vals.get("release_note_ids", [])
                for command in new_release:
                    if command[0] in (4, 6):  # 4 = ajouter, 6 = remplacer
                        raise UserError("You cannot link a task to multiple release notes.")

        res = super(ProjectTask, self).write(vals)

        sprint_urgent = self.env['sprint'].search([('name', '=', 'Urgent')], limit=1)
        sprint_new = self.env['sprint'].search([('name', '=', 'New')], limit=1)

        if not sprint_urgent or not sprint_new:
            raise UserError(_("Please ensure the sprints 'Urgent' and 'New' exist."))

        for task in self:
            # Priorité High (1) & Sprint = New ou vide -> affecter sprint Urgent
            if task.priority == '1' and (task.sprint_id == sprint_new or not task.sprint_id):
                super(ProjectTask, task).write({'sprint_id': sprint_urgent.id})

            # Priorité Low (0) & Sprint = Urgent ou vide -> affecter sprint New
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

    def action_link_task(self):
        """Link a task to the release note"""
        release_note_ids = self.env.context.get("default_release_note_ids")
        if not release_note_ids:
            raise UserError(
                "You need to save the release note before adding tasks to it."
            )
        self.write({"release_note_ids": [(4, release_note_ids)]})

    def action_unlink_task(self):
        """Délier une tâche de la release note"""
        release_note_ids = self.env.context.get("default_release_note_ids")
        if release_note_ids:
            self.write({"release_note_ids": [(3, release_note_ids)]})
        else:
            raise UserError("The release note is not found, try again.")

    @api.depends('user_ids')
    def _compute_assigned_user_id(self):
        for task in self:
            task.assigned_user_id = task.user_ids[:1]

    def _inverse_assigned_user_id(self):
        for task in self:
            if task.assigned_user_id:
                task.user_ids = [Command.set([task.assigned_user_id.id])]
            else:
                task.user_ids = [Command.clear()]