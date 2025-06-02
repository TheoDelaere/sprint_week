{
    "name": "Burniaux Portal Modification",
    "version": "18.0",
    "author": "Burniaux Consulting",
    "license": "AGPL-3",
    "category": "Tools",
    "depends": [
        'portal',
        'documents',
        'accountant',
        'purchase',
        'burniaux_release_note',
        'burniaux_consumed_hours',
        'burniaux_contact_representative'
    ],
    "data": [
        "views/portal_template.xml",
        "views/project_portal_view.xml",
        "views/project_task_portal_view.xml",
        'views/kpi_portal_view.xml',
        'views/maintenance_portal_view.xml',
        'views/assistance_portal_view.xml',
        'views/res_user.xml',
    ],
    "assets": {
        'web.assets_frontend': [
            'burniaux_portal_modif/static/src/css/style.css',
            'burniaux_portal_modif/static/src/img/*',
            'https://cdn.jsdelivr.net/npm/chart.js',
           #'burniaux_portal_modif/static/src/js/project_portal_view.js',
            'burniaux_portal_modif/static/src/js/portal_chart.js',
            'burniaux_portal_modif/static/src/js/project_portal_view.js',
            'burniaux_portal_modif/static/src/js/project_portal_pv.js',
        ],
    },
    "application": False,
    "installable": True,
}
