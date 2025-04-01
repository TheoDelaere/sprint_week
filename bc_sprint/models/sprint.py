from odoo import models, fields, api


class Sprint(models.Model):
    _name = "sprint"
    _description = "Sprint"


    name = fields.Char(string="Sprint Name", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    task_ids = fields.One2many('project.task', 'sprint_id', string="Sprint Tasks")
    team_id = fields.Many2one('sprint.team', string="Sprint Team", store=True)
    color = fields.Integer(string='Color Index', export_string_translation=False)
    show_by_hours_or_number_of_tasks = fields.Selection([
        ('hours', 'Hours'),
        ('tasks', 'Tasks')
    ], string="Show By", default="hours", store=False)
    filter_user_or_team = fields.Selection([
        ('user', 'User'),
        ('team', 'Team')
    ], string="Filter", default="team", store=False)
    user_id = fields.Many2one(
        'res.users', 
        string="Assigned User"
    )
    state_id = fields.Many2one("state", string="State")
    def available_users(self,toto):
        res = [(1, "zaza")]
        print (toto.name)
        for record in toto.team_id.user_ids:
            res.append((record.id, record.name))
            print (record.id, record.name)
        print (res,"####################################################################################")
        return res
    

class SprintTeam(models.Model):
    _name = "sprint.team"
    _description = "Sprint Team"

    name = fields.Char(string="Team Name", required=True)
    sprint_ids = fields.One2many('sprint', 'team_id', string="Sprints")
    user_ids = fields.Many2many('res.users', string="User")

class ProjectTask(models.Model):
    _inherit = "project.task"

    sprint_id = fields.Many2one('sprint', string="Sprint")
