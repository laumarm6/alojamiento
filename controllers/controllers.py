# -*- coding: utf-8 -*-
# from odoo import http


# class Alojamiento(http.Controller):
#     @http.route('/alojamiento/alojamiento/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alojamiento/alojamiento/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alojamiento.listing', {
#             'root': '/alojamiento/alojamiento',
#             'objects': http.request.env['alojamiento.alojamiento'].search([]),
#         })

#     @http.route('/alojamiento/alojamiento/objects/<model("alojamiento.alojamiento"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alojamiento.object', {
#             'object': obj
#         })
