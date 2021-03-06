# -*- coding: utf-8 -*-

{
    'name' : 'Open Academy',
    'version' : '14.0.1.0',
    'summary': 'Manage trainings',
    'sequence': 10,
    'description': """ 
      Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration

      """,
    'category': 'Productivity',
    'website': 'https://www.nava.com.np',
    'images' : ['images/index.png'],
    'depends': [],
    'data': [
      'security/security.xml',
      'security/ir.model.access.csv',
      'views/openacademy.xml',
      'views/partner.xml',
      'wizard/wizard_view.xml'
    ],
    'demo': ['demo/demo.xml'],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    
}
