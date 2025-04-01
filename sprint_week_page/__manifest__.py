{
    'name': "BC Sprint",
    'version': "1.0",
    'author': "Burniaux Consulting",
    'website': "https://www.burniauxconsulting.com/",
    'category': "Project",
    'depends': ['base', 'project'],
    'data': [
        # security
        'security/ir.model.access.csv',

        # views
        'views/sprint_views.xml',
    ],
    'installable': True,
    'application': True,
}
