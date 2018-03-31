from odoo import models, fields,api

class users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'
    pricelist_ids = fields.Many2many('product.pricelist', 'pricelist_security_pricelist_users','user_id','pricelist_id', 'Restricted Pricelists', help="This Pricelists and the information related to it will be only visible for users where you specify that they can see them setting this same field.")
    
