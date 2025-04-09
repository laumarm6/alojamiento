from odoo import models, fields


class Landlords(models.Model):
    _name = 'alojamiento.landlords'
    _description = 'Define cada uno de los propietarios de alojameinto'

    name = fields.Char(string="Nombre")
    status = fields.Char()