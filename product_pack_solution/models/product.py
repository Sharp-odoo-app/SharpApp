# -*- coding: utf-8 -*-
from odoo import models,fields, api
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    
    is_product_pack = fields.Boolean(string="Is Product Pack")
    product_pack_ids = fields.One2many('products.pack', 'product_product_id', string="Pack Products")

    @api.onchange('product_pack_ids')
    def calc_pack_price(self):
        if self.is_product_pack:
            pack_price = 0.0
            for product in self.product_pack_ids:
                pack_price += product.product_id.lst_price * product.quantity
            self.list_price = pack_price


class ProductsPack(models.Model):
    _name = 'products.pack'
    _rec_name = 'product_id'
    _order = 'sequence, product_id'

    sequence = fields.Integer(string='Sequence', default=10)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_product_id = fields.Many2one('product.product', string="Product Relation")
    quantity = fields.Float(string="Quantity", required=True, default=1)

    @api.constrains('quantity')
    def check_quantity(self):
        if self.quantity < 1:
            raise UserError(_('Enter atleast 1 quantity into pack quantity.'))


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_product_pack = fields.Boolean(string="Is Product Pack")

    @api.onchange('is_product_pack')
    def onchange_is_product_pack(self):
        if self.is_product_pack:
            self.type = 'consu'
