# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Tarun Packaging',
    'version': '1.2',
    'author': 'Tarun Behal (PMI)',
    'summary': 'Inventory, Logistic',
    'description' : """
Manage Delivery by Packaging
    """,
    'website': 'http://www.pmi.com',
    'depends': ['product', 'stock', 'account', 'purchase'],
    'category': 'Warehouse Management',
    'sequence': 16,
    'demo': [
    ],
    'data': [
        'tarun_packaging_view.xml',
    ],
    'test': [
#        'test/opening_stock.yml',
#        'test/shipment.yml',
#        'test/stock_report.yml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'css': [ 'static/src/css/stock.css' ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
