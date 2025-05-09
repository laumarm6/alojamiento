from odoo import models, fields


class AccommodationClients(models.Model):

    # herencia por propotipo extiendo la clase pero creo nuevas vistas
    #_name = 'alojamiento.aclients'
    _description = 'Listado de los clientes'
    _inherit = 'res.partner'


# Clientes [1]:[N] Reservas
    booking_ids = fields.One2many('alojamiento.bookings', 'client_id', string ="Reservas")

    accommodation_client = fields.Boolean(string="Cliente de Alojamiento", default=False)
    
    