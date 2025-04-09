from odoo import models, fields


class Accommodations(models.Model):
    _name = 'alojamiento.accommodations'
    _description = 'Define cada uno de los alojameintos'

    name = fields.Char(string="Nombre")
    status = fields.Char()