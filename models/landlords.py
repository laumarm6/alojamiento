from odoo import models, fields, api
from odoo.exceptions import ValidationError


import re
import datetime


class Landlords(models.Model):
    _name = 'alojamiento.landlords'
    _description = 'Define cada uno de los propietarios de alojameinto'

    dni = fields.Char(string = "DNI", size = 9, required = True)
    name = fields.Char(string="Nombre", required = True)
    surname = fields.Char(string="Apellidos")
    address = fields.Text(string = "Dirección")
    phone = fields.Char(string = "Teléfono", size = 9, required = True)
    start_date = fields.Date(string = 'Fecha de alta')
    end_date =fields.Date(string = 'Fecha de baja')
    status = fields.Boolean()
    age = fields.Integer(string = "Antigüedad", compute ='_compute_age')
    number_of_rooms = fields.Integer(string="Nº de habitaciones", compute='_compute_number_of_rooms')

    _sql_constraints = [
    ('dni_uniq', 'unique(dni)', 'El dni debe ser único'),
    ]

# Landlords [1]:[N] Contracts - necesaria?
    contract_ids = fields.One2many('alojamiento.contracts')
# Landlords [1]:[N] Contracts - necesaria?
    accommodation_ids = fields.Many2many('alojamiento.accommodations', string = "Nº de alojamientos")


    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            pattern = re.compile("^\d{8}[A-Z]{1}$")
            if not pattern.match(record.dni):
                raise ValidationError('El formato deben ser NNNNNNNNA donde N un número y A es una letra mayúscula ')

    @api.constrains('phone')
    def _check_phone(self):
            for record in self:
                pattern = re.compile("\d{9}")
                if not pattern.match(record.phone):
                    raise ValidationError('El formato deben ser NNNNNNNNN donde N un número')   

    @api.depends('start_date')
    def _compute_age(self):
            now = datetime.date.today()
            for record in self:
                if record.start_date == False:
                    record.age = 0
                else:
                    dif =(now - record.start_date)
                    record.age = dif.days // 365
    
    @api.depends('accommodation_ids')
    def _compute_number_of_rooms(self):
        for record in self:
            record.number_of_rooms = sum(accommodation.rooms 
                                         for accommodation in record.accommodation_ids)