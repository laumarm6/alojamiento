from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re


class Rooms(models.Model):
    _name = 'alojamiento.rooms'
    _description = 'Define las habitaciones de cada uno de los alojameintos'

    code = fields.Char(string="Identificador habitación", size = 10, required = True)
    name = fields.Char(string = "Nombre", required = True)
    description = fields.Text(string = "Descripción", required=True)
    type = fields.Selection([('SEN','Sencilla'),('DBL','Doble'),('SEB', 'Sencilla con baño'),('DBB', 'Doble con baño')], string= "Tipo",required=True)
    num_beds = fields.Integer(string = "Nº camas", required=True)
    num_bath = fields.Integer(string= "Nº baños", required=True)
    status = fields.Boolean()
    #is_occupied = fields.Boolean(default=False)

    _sql_constraints = [
    ('code_uniq', 'unique(code)', 'El identificador debe ser único'),
    ('name_uniq', 'unique(name)', 'El nombre debe ser único'),
     ]
    
    # Rooms [N]:[1] Accommodations
    accommodation_id = fields.Many2one('alojamiento.accommodations', string="Alojamiento")

    
    
    #poner un identificador automático
    @api.constrains('code')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("^[A-Z]{3}\d{5,}$")
            if not pattern.match(record.code):
                raise ValidationError('El formato deben ser AAANNNNN donde A es una letra mayúscula y N un número')


