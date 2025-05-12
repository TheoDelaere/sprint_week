from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import pdf
import base64


def _get_done_stage_ids(env):
    """
    Helper to fetch all stage IDs that are considered 'done' (folded stages).
    """
    return env['project.task.type'].search([('fold', '=', True)]).ids


class Sprint(models.Model):
    _name = "sprint"
    _description = "Sprint"
    _order = "sequence asc, start_date asc"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Each Sprint name must be unique!')
    ]

    name = fields.Char(string="Name", store=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    year = fields.Integer(string="Year", compute="_compute_year_month_week", store=True)
    month = fields.Integer(string="Month", compute="_compute_year_month_week", store=True)
    week = fields.Integer(string="Week", compute="_compute_year_month_week", store=True)
    sequence = fields.Integer('Sequence', default=21, help="Used to sort the types.")
    color = fields.Integer(string="Color Index", default=10, help="Used to sort archived type.")
    archived = fields.Boolean(string="Archived", default=False, help="Used to sort the types.")

    attachment_id = fields.Many2one('ir.attachment', string="PDF Attachment")
    pdf = fields.Binary(string="PDF", readonly=True)
    pdf_name = fields.Char(string="PDF Name")
    task_history_ids = fields.Many2many('project.task', 'sprint_id', string="Tasks history")
    task_ids = fields.One2many('project.task', 'sprint_id', string="Tasks")
    project_id = fields.Many2one("project.project", string="Project")

    column_type = fields.Selection([
        ('sprint', 'Sprint'),
        ('new', 'New'),
        ('urgent', 'Urgent'),
        ('later', 'Later'),
    ], string="Column Type", default='sprint', help="Used to sort the types.", required=True)

    user_id = fields.Many2one(
        "res.users", string="Created By", default=lambda self: self.env.user
    )

    company_id = fields.Many2one(
        "res.company", string="Company", required=True, default=lambda self: self.env.company.id
    )

    def archive_sprint_and_pass_unfinished_tasks_to_next_sprint(self):
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
            sprint.write({'color': 1})

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

    @api.onchange('archived')
    def _onchange_archived(self):
        if self.archived:
            self.color = 1

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

    def action_kanban(self):
        return {
            'name': 'Sprint Kanban',
            'view_type': 'form',
            'view_mode': 'kanban',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.task_ids.ids)],
            'context': {'search_default_sprint_id': self.id, 'group_by': 'assigned_user_id'},
        }

    def action_print_sprint_release(self):
        """Print the sprint_release"""
        pdf_content = self._generate_pdf_for_sprint_release()
        pdf_base64 = base64.b64encode(pdf_content)

        attachment = self.env['ir.attachment'].create({
            'name': f"Sprint_release{self.name}.pdf",
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
            'type': 'binary'
        })
        self.attachment_id = attachment.id  # Stocke l'ID de l'attachement pour le récupérer plus tard
        self.pdf = pdf_base64
        self.pdf_name = attachment.name
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def _generate_pdf_for_sprint_release(self):
        report = self.env.ref("bc_sprint.action_sprint_release_pdf_report")
        pdf_content, _ = report._render_qweb_pdf(
            "bc_sprint.action_sprint_release_pdf_report", res_ids=self.ids)
        return pdf_content
