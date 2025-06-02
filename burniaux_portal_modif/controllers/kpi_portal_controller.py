from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from odoo.addons.portal.controllers.portal import CustomerPortal



class KPIPortalController(CustomerPortal):

    @http.route(['/my/kpi'], type='http', auth="user", website=True)
    def portal_my_kpi(self, **kw):
        current_url = request.httprequest.url
        user = request.env.user.user_id

        # Factures clients (account.move)
        invoices = request.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),
            ('user_id', '=', user.id),
            ('state', 'in', ['posted'])
        ], limit=10, order='date desc')

        # Commandes d'achat (module Purchase)
        purchases = request.env['purchase.order'].sudo().search([
            ('user_id', '=', user.id),
        ])

        values = {
            'page_name': 'my_kpi',
            'invoices': invoices,
            'purchases': purchases,
            'current_url': current_url,
        }

        return request.render("burniaux_portal_modif.portal_my_kpi", values)

    @http.route(['/my/maintenance'], type='http', auth="user", website=True)
    def portal_my_maintenance(self, **kw):
        current_url = request.httprequest.url
        projects = request.env['project.project'].sudo().search(
            [('project_maintenance_type', '=', True)])

        values = {
            'page_name': 'my_maintenance',
            'current_url': current_url,
            'projects': projects,
        }

        return request.render("burniaux_portal_modif.portal_my_assistance", values)

    @http.route(['/my/assistance'], type='http', auth="user", website=True)
    def portal_my_assistance(self, **kw):
        current_url = request.httprequest.url
        representatives = request.env.user.representative_ids
        if not representatives:
            representatives = request.env['res.users'].sudo().search(
            [('default_support', '=', True)],
                print(request.env['res.users'].sudo().search(
            [('default_support', '=', True)]), "============================================")
        )

        values = {
            'page_name': 'my_assistance',
            'current_url': current_url,
            'representatives': representatives,
        }

        return request.render("burniaux_portal_modif.portal_my_assistance", values)
    @http.route(['/my/assistance/send/mail'], type='http', auth="user", methods=["POST"], website=True)
    def send_mail(self, **kw):
        # Vérification du token CSRF
        if kw.get('csrf_token') != request.session.csrf_token:
            raise AccessDenied("Invalid CSRF token")

        partner = request.env.user.partner_id
        recipient_id = kw.get('recipient_id')
        recipient = request.env['res.partner'].browse(int(recipient_id))
        subject = kw.get('subject', 'Demande d’assistance de ' + partner.name)
        body = kw.get('body')

        if recipient and body:
            mail_values = {
                'subject': subject,
                'body_html': f"<p>{body}</p>",
                'recipient_ids': [(6, 0, [recipient.id])],
                'email_from': partner.email,
            }
            request.env['mail.mail'].create(mail_values).send()
        return request.redirect('/my')
