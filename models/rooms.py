from odoo import models, fields


class Rooms(models.Model):
    _name = 'alojamiento.rooms'
    _description = 'Define las habitaciones de cada uno de los alojameintos'

    name = fields.Char(string="Nombre")
    status = fields.Char()