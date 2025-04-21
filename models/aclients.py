from odoo import models, fields


class AccommodationClients(models.Model):

    # herencia por propotipo extiendo la clase pero creo nuevas vistas
    #_name = 'alojamiento.aclients'
    _description = 'Listado de los clientes'
    _inherit = 'res.partner'


    #accommodation_client = fields.Boolean(string="Cliente de Alojamiento", default=False)
    #room_preference = fields.Selection([
       # ('IND', 'Individual'),
       # ('DBL', 'Doble'),
        #('PRV', 'Con baño privado'),
   # ], string="Preferencia de habitación")
    