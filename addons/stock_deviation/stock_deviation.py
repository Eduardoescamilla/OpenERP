
from openerp.osv import fields,osv

class stock_move(osv.osv):
    _inherit = "stock.move"
    _columns = {
        'pmi_location_id': fields.many2one('stock.location', 'Source Location',states={'done': [('readonly', True)]}, help="Location which is actual source"),
        'pmi_location_dest_id': fields.many2one('stock.location', 'Destination Location',states={'done': [('readonly', True)]}, help="Location which is actual destination"),
    }
stock_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

