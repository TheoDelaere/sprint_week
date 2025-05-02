from odoo import models, fields, api

class SprintRelease(models.Model):
    _name = "sprint.release"
    _description = "Sprint Release"
    _order = "name desc"

    name = fields.Char(string="Sprint Release", required=True)
    release_date = fields.Date(string="Release Date")
    task_ids = fields.One2many("project.task", "release_id", string="Linked Tasks", copy=True)

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