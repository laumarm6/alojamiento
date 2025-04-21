from odoo import models, fields


class Allocations(models.Model):
    _name = 'alojamiento.allocations'
    _description = 'Relación entre reservas, estudiantes y habitaciones asignadas'

    name = fields.Char(string="Nombre")
    room_id = fields.Many2one('alojamiento.rooms', required=True)
    booking_id = fields.Many2one('alojamiento.bookings', required=True)
    student_id = fields.Many2one('alojamiento.students', required=True)
    type = fields.Selection([('AUT', 'Automática'), ('MAN', 'Manual')])
    

    
    
    _sql_constraints = [
        ('unique_assignment', 'unique(booking_id, student_id)',
         'Cada estudiante debe estar asignado una sola vez por reserva.')
    ]
