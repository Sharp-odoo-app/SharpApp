from odoo import models,fields,api

class product_pricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = 'product.pricelist'

    user_ids = fields.Many2many('res.users', 'pricelist_security_pricelist_users', 'pricelist_id', 
            'user_id', string='Restricted to Users', help='If choose some users, then this Pricelist and the information related to it will be only visible for those users.')
    
   
