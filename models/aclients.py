from odoo import models, fields


class AccommodationClients(models.Model):

    # herencia por propotipo extiendo la clase pero creo nuevas vistas
    #_name = 'alojamiento.aclients'
    _description = 'Listado de los clientes con alojamiento y sus características'
    _inherit = 'res.partner'

  # room_preference = fields.Selection([
       # ('SGL', 'Individual'),
       # ('DBL', 'Doble'),
        #('PRV', 'Con baño privado'),
   # ], string="Preferencia de habitación")
   # accommodation_client = fields.Boolean(string="Cliente de Alojamiento", default=False)

   # name = fields.Char(string="Nombre")
    #status = fields.Char()  