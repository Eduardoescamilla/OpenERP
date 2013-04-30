
from openerp.osv import osv


class sale_order(osv.osv): 
    
    def _check_unique_insesitive(self, cr, uid, ids, context=None):
        so_ids = self.search(cr, 1 ,[], context=context)
        lst = []
        to_check = ()
        for x in self.browse(cr, uid, so_ids, context=context):
            if x.client_order_ref and x.id not in ids and x.state not in 'cancel':
                lst += [(x.partner_id.id, x.client_order_ref)] 
        for self_obj in self.browse(cr, uid, ids, context=context):
            to_check = (self_obj.partner_id.id,self_obj.client_order_ref)
            print "to check", to_check
            print "list", lst
            if to_check in lst:
                return False
            return True    
    
    
    _inherit = 'sale.order' 
    _constraints = [(_check_unique_insesitive, 'Error: Customer PO used is not unique. Contact Sales Dept.', ['client_order_ref'])]
    
    



    
sale_order()
