{
    'name': "BC Sprint",
    'version': "18.0",
    "license": "AGPL-3",
    'author': "Burniaux Consulting",
    'website': "https://www.burniauxconsulting.com/",
    'category': "Project",
    'depends': ['base', 'project'],
    'data': [
        # security
        'security/ir.model.access.csv',

        # views
        'views/sprint_week_view.xml',
        'views/sprint_solo_views.xml',
        'views/sprint_state.xml',
        'views/project_task_custom.xml',
        'views/sprint_menu.xml',
    ],
    'installable': True,
    'application': True,
}
