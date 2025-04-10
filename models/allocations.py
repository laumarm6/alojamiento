from odoo import models, fields


class Allocations(models.Model):
    _name = 'alojamiento.allocations'
    _description = 'Define asignaciones de cada reserva a los alojameintos'

    name = fields.Char(string="Nombre")
    status = fields.Char()