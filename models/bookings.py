from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Bookings(models.Model):
    _name = 'alojamiento.bookings'
    _description = 'Registra las reservas hechas'

    name = fields.Char(string="Identificador")
    start_date= fields.Date(string="Fecha inicio")
    end_date= fields.Date(string="Fecha fin")
    status = fields.Char()

    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]
    
    @api.constrains('name')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("\d{3,}")
            if not pattern.match(record.name):
                raise ValidationError('El formato deben ser NNN donde N un número')
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
            for record in self:
                if record.end_date and record.start_date > record.end_date:
                    raise ValidationError("La fecha fin no puede ser anterior a la fecha de inicio.")
