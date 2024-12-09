{
    'name': 'Veterinary Clinic Sales',
    'version': '17.0.1.0.0',
    'description': 'Allow sales of appointments',
    'summary': '',
    'author': '<aleon>',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'veterinary_clinic',
        'sale',
    ],
    # load data in order
    'data': [
        'views/sale_order.xml',
        'views/veterinary_appointment.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}
