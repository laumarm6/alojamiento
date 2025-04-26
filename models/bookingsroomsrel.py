from odoo import models, fields

class BookingsRoomsRel (models.Model):
    _name = 'alojamiento.booking_room_rel'
    _description = 'Relación entre reservas y habitaciones asignadas'

    
    booking_id = fields.Many2one('alojamiento.bookings', string="Reserva", required=True, ondelete='cascade')
    room_id = fields.Many2one('alojamiento.rooms', string="Habitación", required=True, ondelete='cascade')
    student_id = fields.Many2one('alojamiento.students', string="Estudiante", required=True, ondelete='cascade')
    #assigned_date = fields.Date(default=fields.Date.today)
    #type = fields.Selection([('AUT', 'Automática'), ('MAN', 'Manual')], string="Tipo")


    _sql_constraints = [
    ('booking_room_uniq', 'unique(room_id,booking_id)', 'La combinación de reserva y habitación debe ser único'),
    ]
