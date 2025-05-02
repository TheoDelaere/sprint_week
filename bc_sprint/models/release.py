from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SprintRelease(models.Model):
    _name = "sprint.release"
    _description = "Sprint Release"
    _order = "name desc"

    name = fields.Char(string="Sprint Release", required=True)
    release_date = fields.Date(string="Release Date")
    project_id = fields.Many2one("project.project", string="Project")
    task_ids = fields.Many2many("project.task", "release_id", string="Linked Tasks", copy=True)

    available_task_ids = fields.Many2many(
        "project.task",
        string="Available Tasks",
        compute="_compute_available_task_ids",
        store=False,
    )

    user_id = fields.Many2one(
        "res.users", string="Created By", default=lambda self: self.env.user
    )

    user_ids = fields.Many2many(
        "res.users",
        relation="release_note_user_rel",
        column1="release_note_id",
        column2="user_id",
        string="Assignees",
        default=lambda self: [(6, 0, [self.env.user.id])],
        context={"active_test": False},
        domain="[('share', '=', False), ('active', '=', True)]",
    )

    company_id = fields.Many2one(
        "res.company", string="Company", required=True, default=lambda self: self.env.company.id
    )

    @api.depends("project_id", "task_ids")
    def _compute_available_task_ids(self):
        """Lists all project tasks that are not yet linked to the release note"""
        for record in self:
            if record.project_id:
                record.available_task_ids = self.env["project.task"].search(
                    [
                        ("project_id", "=", record.project_id.id),
                        ("release_note_ids", "=", False)
                    ]
                )
            else:
                record.available_task_ids = self.env["project.task"].browse([])

    @api.onchange("project_id")
    def _clear_task_ids(self):
        for record in self:
            record.task_ids = False

    def unlink(self):
        """Prevents deletion if send_status is enabled"""
        for record in self:
            if record.send_status:
                raise UserError(
                    "You cannot delete a Release Note that has already been sent."
                )
        return super(SprintRelease, self).unlink()