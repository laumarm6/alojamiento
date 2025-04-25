from odoo import models, fields,api
from odoo.exceptions import ValidationError


import re


class Students(models.Model):
    _name = 'alojamiento.students'
    _description = 'Relación de estudiantes'

    dni = fields.Char(string = "DNI", size = 9, required = True)
    name = fields.Char(string="Nombre", required = True)
    surname = fields.Char(string="Apellidos")
    address = fields.Text(string = "Dirección")
    phone = fields.Char(string = "Teléfono", size = 9, required = True)
    level = fields.Selection([('LA1','A1'),('LA2','A2'),('LB1', 'B1'),('LB2', 'B2'),('LC1', 'C1'),('LC2', 'C2')])

# Estudiantes [N]:[N] Reservas
    
    booking_id = fields.Many2many('alojamiento.bookings', string="Reservas")
    


    _sql_constraints = [
    ('dni_uniq', 'unique(dni)', 'El dni debe ser único'),
    ]


    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            pattern = re.compile("^\d{8}[A-Z]{1}$")
            if not pattern.match(record.dni):
                raise ValidationError('El formato deben ser NNNNNNNNA donde N un número y A es una letra mayúscula ')