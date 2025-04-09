from odoo import models, fields


class Contratos(models.Model):
    _name = 'alojamiento.contratos'
    _description = 'Define cada uno de los alojamientos para estudiantes'

    name = fields.Char(string="Nombre")
    status = fields.Char()

    