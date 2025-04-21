from odoo import models, fields


class AccommodationClients(models.Model):
    _name = 'alojamiento.aclients'
    _description = 'Listado de los cleintes con alojamiento y sus características'

    name = fields.Char(string="Nombre")
    status = fields.Char()