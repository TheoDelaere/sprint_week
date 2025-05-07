from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import pdf
import base64

class ReleaseNote(models.Model):
    _name = "release.note"
    _description = "Release Note"
    _order = "name desc"

    name = fields.Char(string="Release notes", required=True)
    release_date = fields.Date(string="Release Date")
    task_ids = fields.Many2many("project.task", string="Linked Tasks", copy=True)
    project_id = fields.Many2many("project.project", string="Project")
    attachment_id = fields.Many2one('ir.attachment', string="PDF Attachment")

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

        """Ajouter condition à la supression"""

        return super(ReleaseNote, self).unlink()

    def action_print_release_note(self):
        """Print the release note"""
        pdf_content = self._generate_pdf_for_release_note()
        pdf_base64 = base64.b64encode(pdf_content)

        attachment = self.env['ir.attachment'].create({
            'name': f"Release_Note_{self.name}.pdf",
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
            'type': 'binary'
        })
        self.attachment_id = attachment.id  # Stocke l'ID de l'attachement pour le récupérer plus tard
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def _generate_pdf_for_release_note(self):
        report = self.env.ref("bc_sprint.action_release_note_pdf_report")
        pdf_content, _ = report._render_qweb_pdf(
            "bc_sprint.action_release_note_pdf_report", res_ids=self.ids)
        return pdf_content