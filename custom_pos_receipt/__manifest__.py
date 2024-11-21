{
    'name': 'Custom POS Receipt',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Custom receipt format for POS',
    'description': """
        This module modifies the default POS receipt template.
    """,
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'web'],
    'data': [
        'views/invoice_layout.xml',
        'report/pos_invoice_report.xml',
    ],
    'assets': {
        # 'web.assets_backend': [
        #     'custom_pos_receipt/static/src/css/pos_receipt.css',
        # ],
        'point_of_sale.assets': [
            'custom_pos_receipt/static/src/css/pos_receipt.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}