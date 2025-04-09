from odoo import models, fields


class Contracts(models.Model):
    _name = 'alojamiento.contracts'
    _description = 'Define cada uno de los alojamientos para estudiantes'

    name = fields.Char(string="Nombre")
    status = fields.Char()

    