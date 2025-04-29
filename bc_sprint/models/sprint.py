from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class Sprint(models.Model):
    _name = "sprint"
    _description = "Sprint"
    _order = "sequence asc, start_date asc"

    name = fields.Char(string="Name", compute="compute_name", store="True")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    year = fields.Integer(string="Year", compute="_compute_year_month_week", store=True)
    month = fields.Integer(string="Month", compute="_compute_year_month_week", store=True) #useless field but kept for future use maybe to segment the year in trimesters or something like that
    week = fields.Integer(string="Week", compute="_compute_year_month_week", store=True)
    sequence = fields.Integer('Sequence', default=10, help="Used to sort the types.")
    color = fields.Integer(string="Color Index")
    task_history_ids = fields.Many2many('project.task', 'sprint_id', string="Tasks")
    task_ids = fields.One2many('project.task', 'sprint_id', string="Tasks")
    sequence = fields.Integer('Sequence', default=21, help="Used to sort the types.")
    archived = fields.Boolean(string="Archived", default=False, help="Used to sort the types.")
    column_type = fields.Selection([
        ('sprint', 'Sprint'),
        ('new', 'New'),
        ('urgent', 'Urgent'),
        ('later', 'Later'),
    ], string="Column Type", default='sprint', help="Used to sort the types.", required=True)

    @api.constrains('archived')
    def _check_archived(self):
        for record in self:
            if record.archived and not self.env.context.get('bypass_archived_check', False):
                raise ValidationError("Archived sprints cannot be edited.")

    @api.onchange('start_date')
    def _start_date_on_monday(self):
        for record in self:
            if record.start_date:
                date_obj = self.start_date
                if date_obj.weekday() != 0:
                    date_obj = date_obj - timedelta(days=date_obj.weekday())
                record.start_date = date_obj

    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                date_obj = record.start_date
                record.end_date = date_obj + timedelta(days=5)
            else:
                record.end_date = False

    @api.depends('start_date')
    def _compute_year_month_week(self):
        for record in self:

            if record.start_date:
                date_obj = self.start_date
                record.year = date_obj.year
                record.week = date_obj.isocalendar()[1]
                record.month = date_obj.month
            else:
                record.year = 0
                record.week = 0

    @api.depends('start_date')
    def compute_name(self):
        for record in self:
            if record.week and record.year:
                record.name = f"{record.year} Week {record.week if record.week > 9 else '0' + str(record.week)} sprint"



    def action_graph(self):
        return {
            'name': 'Sprint Graph',
            'view_type': 'form',
            'view_mode': 'graph',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.task_ids.ids)],
            'context': {
            'search_default_sprint_id': self.id,
            }
        }

    def action_schedule(self):
        return {
            'name': 'Sprint Schedule',
            'view_type': 'form',
            'view_mode': 'gantt',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [
                ('id', 'in', self.task_ids.ids),
            ],
            'context': {
                'search_default_sprint_id': self.id,
            }
        }
            



    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Each Sprint name must be unique!')
    ]
