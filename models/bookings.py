from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Bookings(models.Model):
    _name = 'alojamiento.bookings'
    _description = 'Registra las reservas hechas'

    name = fields.Char(string="Identificador", required=True)
    start_date= fields.Date(string="Fecha inicio", required=True)
    end_date= fields.Date(string="Fecha fin", required=True)
    status = fields.Selection([('PEN', 'Pendiente'), ('CONF', 'Confirmada'), ('CANC', 'Cancelada')], default='PEN')
    days = fields.Integer(string="Duración", compute='_compute_days')
    


    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]
    
    # Bookings [N]:[1] Clients
    client_id = fields.Many2one('alojamiento.aclients', string = "Cliente")

    # Bookings [N]:[N] Estudiantes
    students_ids = fields.Many2many('alojamiento.students', string = "Estudiantes")

    # Bookings [N]:[N] Habitaciones
    rooms_ids = fields.Many2many('alojamiento.rooms', string = "Habitaciones")
    
    
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
    
    @api.depends('start_date', 'end_date')
    def _compute_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.days = (record.end_date - record.start_date).days
            else:
                record.days = 0



