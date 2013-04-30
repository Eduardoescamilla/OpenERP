from openerp.osv import osv, fields

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _columns = {
        'tarun_distributor': fields.char('Distributor', size=128),
        'sale_kit': fields.selection([ ('no', 'NO'),
                                    ('yes', 'YES'),],
                        string='Sample Sent', size=16,
                        help='Select option based on Sample Kit, If sent select Yes'),
    }


crm_lead()
