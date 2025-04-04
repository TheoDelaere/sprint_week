from odoo import models, fields, api, _


class Sprint(models.Model):
    _name = "sprint"
    _description = "Sprint"

    name = fields.Char(string="Sprint Name", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    task_ids = fields.One2many('project.task', 'sprint_id', string="Sprint Tasks")
    week_ids = fields.One2many('sprint.week', inverse_name='sprint_id', string="Week")
    color = fields.Integer(string='Color Index', export_string_translation=False)
    show_by_hours_or_number_of_tasks = fields.Selection([
        ('hours', 'Hours'),
        ('tasks', 'Tasks')
    ], string="Show By", default="hours", store=False)
    user_id = fields.Many2one(
        'res.users',
        string="Assigned User"
    )
