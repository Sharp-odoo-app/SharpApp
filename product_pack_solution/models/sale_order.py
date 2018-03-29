# -*- coding: utf-8 -*-
from itertools import groupby
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_pack_line = fields.One2many('products.pack.line', 'order_id',
                                        states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                        copy=True)


    @api.multi
    def pack_lines_layouted(self):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(self.product_pack_line, lambda l: l.layout_category_id):
            # If last added category induced a pagebreak, this one will be on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })

        return report_pages

    @api.multi
    def action_confirm(self):
        self.create_boq_from_packline()
        res = super(SaleOrder, self).action_confirm()
        return res

    @api.multi
    def create_boq_from_packline(self):
        if self.product_pack_line:
            self.compute_pack_price()
            for l in self.order_line:
                l.unlink()
            for line in self.product_pack_line:
                if line.is_product_pack and line.product_id.product_pack_ids:
                    for pack_line in line.product_id.product_pack_ids:
                        order_line = self.env['sale.order.line'].search([('order_id','=',self.id),('product_id','=', pack_line.product_id.id)])
                        if order_line:
                            qty = order_line[0].product_uom_qty + pack_line.quantity * line.product_uom_qty
                            order_line[0].write({'product_uom_qty':qty})
                        else:
                            vals = {
                            'product_id': pack_line.product_id.id,
                            'product_uom_qty': pack_line.quantity * line.product_uom_qty,
                            'order_id': self.id,
                            'tax_id':[(6, 0, line.tax_id.ids)],
                            }
                            order_line_id = order_line.create(vals)
                else:
                    order_line = self.env['sale.order.line'].search([('order_id','=',self.id),('product_id','=', line.product_id.id)])
                    if order_line:
                        qty =  order_line[0].product_uom_qty + line.product_uom_qty
                        order_line[0].write({'product_uom_qty':qty})
                    else:
                        vals = {
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.product_uom_qty,
                            'order_id':self.id,
                            'tax_id':[(6, 0, line.tax_id.ids)],

                        }
                        order_line_id = order_line.create(vals)
                if line.is_product_pack and line.extra_product_ids:
                    for extra_line in line.extra_product_ids:
                        order_line = self.env['sale.order.line'].search([('order_id','=',self.id),('product_id','=', extra_line.product_id.id)])
                        if order_line:
                            qty = order_line[0].product_uom_qty + extra_line.quantity * line.product_uom_qty
                            order_line[0].write({'product_uom_qty':qty})
                        else:
                            vals = {
                            'product_id': extra_line.product_id.id,
                            'product_uom_qty': line.product_uom_qty * extra_line.quantity,
                            'order_id': self.id,
                            'tax_id':[(6, 0, line.tax_id.ids)],
                            }
                            order_line_id = order_line.create(vals)
        else:
            for l in self.order_line:
                l.unlink()

    def compute_pack_price(self):
        for l in self.product_pack_line:
            if l.is_product_pack:
                pack_price = 0.0
                for p in l.product_id.product_pack_ids:
                    price, rule_id = self.pricelist_id.get_product_price_rule(p.product_id, p.quantity or 1.0, self.partner_id)
                    pack_price += price * p.quantity
                if l.extra_product_ids:
                    for e in l.extra_product_ids:
                        price, rule_id = self.pricelist_id.get_product_price_rule(e.product_id, e.quantity or 1.0, self.partner_id)
                        pack_price += price * e.quantity
                l.price_unit = pack_price
            else:
                price, rule_id = self.pricelist_id.get_product_price_rule(l.product_id, l.product_uom_qty or 1.0, self.partner_id)
                l.price_unit = price

    @api.multi
    def button_dummy(self):
        self.create_boq_from_packline()
        return True





class ProductsPackLine(models.Model):
    _name = 'products.pack.line'
    _inherit = 'sale.order.line'

    is_product_pack = fields.Boolean(compute='_get_is_product_pack')
    extra_product_ids = fields.One2many('extra.product.line', 'pack_line_id')
    layout_category_id = fields.Many2one('sale.layout_category', string='Section')
    section_id = fields.Many2one('pack.section', string='Section')
    line_id = fields.Many2one('pack.line', string='Line')
    side_id = fields.Many2one('pack.side', string='Side')
    type_of_goods_id = fields.Many2one('pack.type.of.goods', string='Type Of Goods')

    @api.multi
    def divide_section(self, layout_category):
        product_pack_lines = layout_category['lines']
        resList = []
        section_ids = []
        for prod in product_pack_lines:
            if prod.section_id not in section_ids:
                section_ids.append(prod.section_id)

        for section in section_ids:
            res = {}
            prod_list = []
            section_total = 0
            for product_line in product_pack_lines:
                if section.id == product_line.section_id.id:
                    prod_list.append(product_line)
                    section_total = section_total + product_line.price_subtotal

            res['section'] = section
            res['prod_list'] = prod_list
            res['section_total'] = section_total
            resList.append(res)
        layout_category['lines'] = resList
        return layout_category

    @api.one
    def _get_is_product_pack(self):
        self.is_product_pack = self.product_id.is_product_pack

    @api.multi
    def action_extra_products(self):
        view_id = self.env['ir.model.data'].xmlid_to_res_id(
            'extra_products_form')
        view = {
            'name': _('Extra Products'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'products.pack.line',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'res_id': self.id,
            'context': self.env.context
        }
        return view

    @api.multi
    def button_save_data(self):
        return True



class ExtraProductLine(models.Model):
    _name = 'extra.product.line'
    _order = 'sequence, product_id'

    sequence = fields.Integer(string='Sequence', default=10)    
    pack_line_id = fields.Many2one('products.pack.line')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float(default=1)

    @api.constrains('quantity')
    def check_quantity(self):
        if self.quantity < 1:
            raise UserError(_('Enter atleast 1 quantity into pack quantity.'))



class wizard_add_pack_line(models.TransientModel):
    _name = 'wizard.add.pack.line'

    pack_id = fields.Many2one('product.product', string="Pack", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1)

    @api.constrains('quantity')
    def check_quantity(self):
        if self.quantity < 1:
            raise UserError(_('Enter atleast 1 quantity into pack quantity.'))

    @api.one
    def add_pack_line(self):
        if self._context.get('active_id'):
            product_pack_line = []
            order_id = self.env['sale.order'].browse(self._context.get('active_id'))
            pack = self.pack_id
            product_pack_line = [
                (0, 0, {'product_id': pack.id,'product_uom_qty': self.quantity})]
            if product_pack_line:
                order_id.write({'product_pack_line':product_pack_line})


class PackSection(models.Model):
    _name = 'pack.section'

    name = fields.Char(string='Section')



class PackLine(models.Model):
    _name = 'pack.line'

    name = fields.Char(string='Line')


class PackSide(models.Model):
    _name = 'pack.side'

    name = fields.Char(string='Side')


class PackTypeOfGoods(models.Model):
    _name = 'pack.type.of.goods'

    name = fields.Char(string='Type Of Goods')