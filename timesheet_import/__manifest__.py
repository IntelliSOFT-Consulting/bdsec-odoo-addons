{
    'name': 'Timesheet Import',
    'version': '1.0',
    'summary': 'Import timesheets from CSV files',
    'description': """
        Module to import timesheets from CSV files.
    """,
    'depends': ['base', 'project','hr_timesheet'],
    'data': [
        'security/timesheet_import_security.xml',
        'views/timesheet_import_views.xml',
    ],
    'installable': True,
    'application': False,
}
