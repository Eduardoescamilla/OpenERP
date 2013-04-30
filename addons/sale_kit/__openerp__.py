
{
    'name': 'Sale Kit',
    'version': '1.0',
    'category': 'Sale',
    'description': """
This module adds a shortcut on one or several opportunity cases in the CRM.
===========================================================================

This shortcut allows you to generate a sales order based on the selected case.
If different cases are open (a list), it generates one sale order by case.
The case is then closed and linked to the generated sales order.

We suggest you to install this module, if you installed both the sale and the crm
modules.
    """,
    'author': 'Tarun Behal',
    'website': 'http://www.pmi.com',
    'images': [],
    'depends': ['crm'],
    'data': [
        'sale_kit_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
