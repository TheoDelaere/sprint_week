{
    'name': "BC Sprint",
    'version': "18.0",
    "license": "AGPL-3",
    'author': "Burniaux Consulting",
    'website': "https://www.burniauxconsulting.com/",
    'category': "Project",
    'depends': ['base', 'project', 'web'],
    'data': [
        # security
        'security/ir.model.access.csv',

        # views
        'views/sprint_week_view.xml',
        'views/sprint_solo_views.xml',
        'views/sprint_state.xml',
        'views/project_task_custom.xml',
        'views/custom_kanban_button.xml',
        'views/sprint_menu.xml',
    ],
    'assets': {
        'web.assets_backend':[
            '/bc_sprint/static/src/js/custom_kanban_button.js',
        ]
    },
    'installable': True,
    'application': True,
}
