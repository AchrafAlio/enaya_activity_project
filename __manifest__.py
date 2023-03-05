# -*- coding: utf-8 -*-
{
    'name': 'Activity Execution Request',
    'version': '1.0',
    'sequence': -100,
    'description': """Enayah Software""",
    'category': 'Productivity/Discuss',
    'website': 'https://www.softifi.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'hr','project'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/modif_notification.xml',
        'data/activity_created_notification.xml',
        'wizard/modify_activity_view.xml',
        'wizard/senior_management_approve_view.xml',
        'views/activity_view.xml',
        'views/sponsor_type_view.xml',
        'views/sponsor_view.xml',
        'views/program_project_view.xml',
        'report/sponsor_speach.xml',
        'views/menu.xml'

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}