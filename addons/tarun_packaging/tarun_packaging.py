
from openerp.osv import fields, osv
import time
import datetime
from datetime import timedelta


class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    _columns = {
        'carrier_fixed': fields.boolean('Carrier Booked', help="If checked, means Carrier is reserved to process this Delivery Order."),
        'spots' : fields.float('No. of Spots', help='Total Number of Spots to be booked at Carrier'),
        'spots_by_computation' : fields.float('Spots as per computation',readonly=True, help='Total Number of Spots automatically computed by system'),
        'spots_fixed': fields.boolean('Spots Fixed', help="If checked, means Final Calculation of Spots id done to process this Delivery Order."),
        'tarun_carrier_ref': fields.char('Carrier Tracking Ref.', size=64, help="Carrier Reference for this Delivery"),
        'tarun_final_carrier_id':fields.many2one('res.partner', 'Carrier', states={'done':[('readonly',True)]},
            change_default=True, track_visibility='always'),
        'tarun_pos' : fields.one2many('purchase.order','tarun_delivery_id','Related RFQs', help='Related RFQ to Carrier'),
        'tarun_spots_computaion' : fields.one2many('tarun.delivery.spots','tarun_delivery_id','Spots Computation', help='Spots are computed based on total products/products in LTL Spots(defined for Products)'),
        'tarun_carrier_date': fields.datetime('Carrier Picking Date', help="Date of picking fixed by Carrier", states={'done':[('readonly', True)], 'cancel':[('readonly',True)]}),
        'tarun_carrier_ids' : fields.many2many('res.partner','tarun_delivery_partner_rel', 'tarun_carrier_id', 'partner_id', 'Carriers Opted', help='Carriers who would process this delivery'),               
        'tarun_notes' : fields.text('Notes', size=64),    
        'tarun_carrier_exception': fields.boolean('Carrier Exception(If any)', help="If any issue related to Carrier in Delivery."),
    }
    
    
            
    def button_spots_compute(self, cr, uid, ids, context=None):
        
        tds = self.pool.get('tarun.delivery.spots')  
        for do in self.browse(cr, uid, ids, context=context):
            spots = 0.0  #to store total spots
            product_spots = 0.0 #to store total product spots
            if do.spots_fixed:
                return
            else:
                for moves in do.move_lines:
                    if moves.product_id.packaging:
                        for pack in moves.product_id.packaging:
                            product_spots = (moves.product_qty/pack.qty) * pack.tarun_ltl_spots
                    else :
                        product_spots = moves.product_qty/40.00     
                    product_spots_str = str(product_spots)                 
                    tds.create(cr, uid, {
                                                        'product_id': moves.product_id.id,
                                                        'ltl_spots': product_spots_str,
                                                        'tarun_delivery_id': do.id,
                                                        })
                    spots +=product_spots                    
                c,m = divmod(spots,1)
                if(m==0):
                    spots = c
                else :
                    spots = (c + 1)     
                value = {'spots_fixed': True,
                         'spots': spots,
                         'spots_by_computation': spots,
                                        }
                return self.write(cr,uid,ids,value,context=context)
            
            
    def button_dummy(self, cr, uid, ids, workcenter_id, context=None):
        
            po = self.pool.get('purchase.order')
            purchase_order_line = self.pool.get('purchase.order.line')
            res_partner = self.pool.get('res.partner')                      
            for do in self.browse(cr, uid, ids, context=context): 
                if do.carrier_fixed:
                    raise osv.except_osv(('Warning!'), ('Carrier already Fixed for this Delivery!'))                    
                    return False
                elif do.spots_fixed == False:
                    raise osv.except_osv(('Warning!'), ('Number of Spots are not computed!'))                    
                    return False                    
                else: 
                    for carriers in do.tarun_carrier_ids: 
                        carrier = res_partner.browse(cr, uid, carriers.id, context=context) 
                        carrier_pricelist = carrier.property_product_pricelist_purchase or False 
                        po_desc = "Spots to "+ str(do.partner_id.city)
                        po_id = po.create(cr, uid, {
                                                    'origin': do.name,
                                                    'tarun_delivery_id': do.id,
                                                    'partner_id': carrier.id,
                                                    'pricelist_id': carrier_pricelist.id,
                                                    'company_id': do.company_id.id,
                                                    'fiscal_position': carrier.property_account_position and carrier.property_account_position.id or False,
                                                    'location_id': '1',
                        
                                                    })
                        # Current date if in case expected date in not there\
                        now = datetime.datetime.now() + timedelta(days=3)
                        po_date = now.strftime("%Y-%m-%d")
                        # Extract the expected date from Delivery Order to schedule a delivery
                        if do.date_expect:                        
                            expected_date = do.date_expect
                            strip_date = expected_date[0:10]
                            po_date = strip_date
                        purchase_order_line.create(cr, uid, {
                                                                 'order_id': po_id,
                                                                 'name': po_desc,
                                                                 'product_qty': do.spots,
                                                                 'price_unit': "0.0",
                                                                 'date_planned': po_date,
                                                                 'product_uom': "1",
                                                                 }, context=context)
                         
                    return True
                
                
            
    def button_check_status(self, cr, uid, ids, workcenter_id, context=None):            
            for do in self.browse(cr, uid, ids, context=context):
                value ={}
                for lines in do.tarun_pos:                     
                    if lines and do.carrier_fixed==False:
                        if lines.state in 'confirmed,done,approved' :
                            value = {'carrier_fixed':True,
                                     'tarun_final_carrier_id':lines.partner_id.id,
                                     'tarun_carrier_ref':lines.partner_ref,
                                     }
                            return self.write(cr,uid,ids,value,context=context)                          
                            
                        #else:
                            #raise osv.except_osv(('Notification!'), ('Carrier confirmation in progress for this Delivery!'))                    
                            
                return True      
                
                
        
        
    _defaults = {
        'carrier_fixed': False,
    }
stock_picking_out()    
# Purchase order Relation Field    
class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    _columns = {
        'tarun_delivery_id': fields.many2one('stock.picking.out', 'Delivery Order Linked'),
    }

purchase_order()
# Product Spots Field    
class product_packaging(osv.osv):
    _inherit = 'product.packaging'
    _columns = {
        'tarun_ltl_spots': fields.float('per LTL spot', help='per LTL Spots to be booked at Carrier for products'),
    }
    _defaults = {
        'tarun_ltl_spots': 1.0,
    }    
product_packaging()    

    
class tarun_delivery_spots(osv.osv):
    _name = "tarun.delivery.spots"
    _description = "Tarun Delivery Spots Computation"
        
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'ltl_spots': fields.char('LTL Spots', size=64, help="Total Number LTL Spots for this product"),
        'tarun_delivery_id': fields.many2one('stock.picking.out', 'Delivery Order Linked'),
    }

tarun_delivery_spots()
    
    