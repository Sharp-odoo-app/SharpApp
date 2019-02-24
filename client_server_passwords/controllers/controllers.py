# -*- coding: utf-8 -*-
from odoo import http

# class ClientServerPasswords(http.Controller):
#     @http.route('/client_server_passwords/client_server_passwords/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/client_server_passwords/client_server_passwords/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('client_server_passwords.listing', {
#             'root': '/client_server_passwords/client_server_passwords',
#             'objects': http.request.env['client_server_passwords.client_server_passwords'].search([]),
#         })

#     @http.route('/client_server_passwords/client_server_passwords/objects/<model("client_server_passwords.client_server_passwords"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('client_server_passwords.object', {
#             'object': obj
#         })