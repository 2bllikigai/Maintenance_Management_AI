{
    'name': 'Asset AI Management',
    'version': '1.0',
    'summary': 'Asset management with depreciation and AI maintenance prediction',

    'depends': [
        'base',
        'hr',
        'account'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/asset_views.xml',
        'views/maintenance_views.xml',
        'data/cron.xml'
    ],

    'installable': True,
    'application': True,
}