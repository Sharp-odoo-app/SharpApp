# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    server_ids = fields.One2many('customer.server.data', 'customer_id')


class CustomerServerData(models.Model):
    _name = 'customer.server.data'

    customer_id = fields.Many2one('res.partner', ondelete='cascade', index=True)
    name = fields.Char()
    url = fields.Char()
    ip = fields.Char(required=True)
    user_name = fields.Char(required=True)
    password = fields.Char(required=True)
