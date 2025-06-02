from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    default_support = fields.Boolean(string="Default Support", default=False)

    def get_total_client_tasks(self):
        """Retourne le nombre total de tâches associées aux projets du client connecté."""
        print("========================================================= azudbin ===================================================")
        user = self.env.user

        # Récupérer tous les projets liés au partenaire du client
        projects = self.env['project.project'].search(
            [('partner_id', 'in', [user.partner_id.id, user.company_id.partner_id.id])])
        task_count = 0
        for project in projects:
            task_count += project.task_count
        # Récupérer toutes les tâches des projets liés
        return task_count

    def get_completed_client_tasks(self):
        """Retourne le nombre de tâches terminées associées aux projets du client connecté."""
        user = self.env.user

        # Récupérer tous les projets liés au partenaire du client
        projects = self.env['project.project'].search(
            [('partner_id', 'in', [user.partner_id.id, user.company_id.partner_id.id])])
        task_count = 0
        for project in projects:
            task_count += project.closed_task_count
        # Récupérer toutes les tâches des projets liés
        return task_count
