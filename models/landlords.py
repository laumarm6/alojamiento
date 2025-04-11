from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re


class Landlords(models.Model):
    _name = 'alojamiento.landlords'
    _description = 'Define cada uno de los propietarios de alojameinto'

    dni = fields.Char(string = "DNI", size = 9, required = True)
    name = fields.Char(string="Nombre", required = True)
    surname = fields.Char(string="Apellidos")
    address = fields.Text(string = "Dirección")
    phone = fields.Char(string = "Teléfono", size = 9, required = True)
    status = fields.Boolean()

    _sql_constraints = [
    ('dni_uniq', 'unique(dni)', 'El dni debe ser unico'),
    ]

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