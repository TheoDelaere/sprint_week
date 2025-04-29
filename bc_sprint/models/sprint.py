from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


def _get_done_stage_ids(env):
    """
    Helper to fetch all stage IDs that are considered 'done' (folded stages).
    """
    return env['project.task.type'].search([('fold', '=', True)]).ids


class Sprint(models.Model):
    _name = "sprint"
    _description = "Sprint"
    _order = "sequence asc, start_date asc"

    name = fields.Char(string="Name", compute="compute_name", store=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    year = fields.Integer(string="Year", compute="_compute_year_month_week", store=True)
    month = fields.Integer(string="Month", compute="_compute_year_month_week", store=True)
    week = fields.Integer(string="Week", compute="_compute_year_month_week", store=True)
    sequence = fields.Integer('Sequence', default=21, help="Used to sort the types.")
    color = fields.Integer(string="Color Index")
    task_history_ids = fields.Many2many('project.task', 'sprint_id', string="Tasks")
    task_ids = fields.One2many('project.task', 'sprint_id', string="Tasks")
    archived = fields.Boolean(string="Archived", default=False, help="Used to sort the types.")
    column_type = fields.Selection([
        ('sprint', 'Sprint'),
        ('new', 'New'),
        ('urgent', 'Urgent'),
        ('later', 'Later'),
    ], string="Column Type", default='sprint', help="Used to sort the types.", required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Each Sprint name must be unique!')
    ]

    def achive_sprint_and_pass_unfinished_tasks_to_next_sprint(self):
        """
        Archive this sprint (and the previous one), and move unfinished tasks to the next sprint.
        """
        today = fields.Date.today()
        for sprint in self:
            if not sprint.start_date or sprint.start_date > today:
                # Cannot archive a sprint that hasn't started yet
                raise ValidationError("Cannot archive sprint before its start date.")

            # 1) Move unfinished tasks forward
            sprint._pass_unfinished_tasks_to_next_sprint()

            # 2) Archive this sprint
            sprint.with_context(bypass_archived_check=True).write({'archived': True})

            # 3) Archive previous sprint, if exists
            prev_start = sprint.start_date - timedelta(days=7)
            prev = self.search([('start_date', '=', prev_start)], limit=1)
            if prev:
                prev.with_context(bypass_archived_check=True).write({'archived': True})

    def _pass_unfinished_tasks_to_next_sprint(self):
        """
        Identify the next sprint by adding 7 days, create it if missing,
        and pass all unfinished tasks into that sprint (without archiving current sprint).
        """
        for sprint in self:
            if not sprint.start_date:
                continue

            # Determine next sprint start
            next_start = sprint.start_date + timedelta(days=7)
            next_sprint = self.search([('start_date', '=', next_start)], limit=1)
            if not next_sprint:
                # Create the new sprint record
                next_sprint = self.create({'start_date': next_start})

            # Determine finished stages
            done_stage_ids = _get_done_stage_ids(self.env)

            # Filter unfinished tasks
            unfinished = sprint.task_ids.filtered(lambda t: t.stage_id.id not in done_stage_ids)
            if unfinished:
                # Reassign to next sprint
                unfinished.write({'sprint_id': next_sprint.id})

    @api.constrains('archived')
    def _check_archived(self):
        for record in self:
            if record.archived and not self.env.context.get('bypass_archived_check', False):
                raise ValidationError("Archived sprints cannot be edited.")

    @api.onchange('start_date')
    def _start_date_on_monday(self):
        for record in self:
            if record.start_date:
                date_obj = record.start_date
                if date_obj.weekday() != 0:
                    date_obj -= timedelta(days=date_obj.weekday())
                record.start_date = date_obj

    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                record.end_date = record.start_date + timedelta(days=5)
            else:
                record.end_date = False

    @api.depends('start_date')
    def _compute_year_month_week(self):
        for record in self:
            if record.start_date:
                record.year = record.start_date.year
                record.week = record.start_date.isocalendar()[1]
                record.month = record.start_date.month
            else:
                record.year = record.week = record.month = 0

    @api.depends('start_date')
    def compute_name(self):
        for record in self:
            if record.week and record.year:
                wk = str(record.week).zfill(2)
                record.name = f"{record.year} Week {wk} sprint"
            else:
                record.name = False

    def action_graph(self):
        return {
            'name': 'Sprint Graph',
            'view_type': 'form',
            'view_mode': 'graph',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.task_ids.ids)],
            'context': {'search_default_sprint_id': self.id},
        }

    def action_schedule(self):
        return {
            'name': 'Sprint Schedule',
            'view_type': 'form',
            'view_mode': 'gantt',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.task_ids.ids)],
            'context': {'search_default_sprint_id': self.id},
        }
