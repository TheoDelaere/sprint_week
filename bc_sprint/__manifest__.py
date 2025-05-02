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
        'views/sprint_history_views.xml',
        'views/project_task_custom.xml',
        'views/sprint_release_view.xml',
        'views/sprint_menu.xml',

        # datas
        'data/sprint_data.xml',
        'data/ir_cron_generate_next_3_sprints.xml',
    ],
    'assets': {
        'web.assets_backend':[
            '/bc_sprint/static/src/js/custom_kanban_button.js',
            '/bc_sprint/static/src/xml/custom_kanban_button.xml',
        ]
    },
    'installable': True,
    'application': True,
}
