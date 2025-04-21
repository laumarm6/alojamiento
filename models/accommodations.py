from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Accommodations(models.Model):
    _name = 'alojamiento.accommodations'
    _description = 'Define cada uno de los alojamientos'

    code = fields.Char(string="Identificador alojamiento", size = 10, required = True)
    name = fields.Char(string = "Nombre", required = True)
    address = fields.Char(string = "Dirección", required=True)
    description = fields.Text(string = "Descripción", required=True)
    rooms = fields.Integer(string="Nº de habitaciones")
    type = fields.Selection([('APT','Apartamento'),('RES','Residencia'),('FAM', 'Familia')], required=True)
    start_date = fields.Date(string = 'Fecha de alta')
    end_date =fields.Date(string = 'Fecha de baja')
    status = fields.Boolean()

    _sql_constraints = [
    ('code_uniq', 'unique(code)', 'El identificador debe ser único'),
    ('name_uniq', 'unique(name)', 'El nombre debe ser único'),
     ]


    # Accommodations [1]:[N] Maintenanceissues
    issues_ids = fields.One2many('alojamiento.maintenanceissues', 'accommodation_id', string = "Incidencias")

    # Accommodations [1]:[N] Rooms
    rooms_ids = fields.One2many('alojamiento.rooms', 'accommodation_id', string="Habitaciones")

    # Accommodations [N]:[N] Landlords 
    landlord_ids = fields.Many2many('alojamiento.landlords', string="Propietarios")
    
    #poner un identificador automático
    @api.constrains('code')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("^[A-Z]{3}\d{5,}$")
            if not pattern.match(record.code):
                raise ValidationError('El formato deben ser AAANNNNN donde A es una letra mayúscula y N un número')
    
    @api.constrains('rooms')
    def _check_rooms(self):
        for record in self:
            if record.rooms < 0:
             raise ValidationError("El número de habitaciones no puede ser negativo.")
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
            for record in self:
                if record.end_date and record.start_date > record.end_date:
                    raise ValidationError("La fecha de baja no puede ser anterior a la fecha de alta.")
                

    @api.constrains('owner_ids')
    def _check_owner(self):
        for record in self:
            if not record.landlord_ids:
             raise ValidationError("Debe haber al menos un propietario asignado al alojamiento.")