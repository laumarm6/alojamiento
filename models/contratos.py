from odoo import models, fields


class Contratos(models.Model):
    _name = 'alojamiento.contratos'
    _description = 'Define cada uno de los alojamientos para estudiantes'

    idContrato = fields.Char(string='Codigo del contrato')
    status = fields.Char()

    