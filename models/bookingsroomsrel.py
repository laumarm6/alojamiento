import logging
from odoo import models, fields, api



class BookingsRoomsRel (models.Model):
    _name = 'alojamiento.booking_room_rel'
    _description = 'Relación entre reservas y habitaciones asignadas'

    
    booking_id = fields.Many2one('alojamiento.bookings', string="Reserva", required=True, ondelete='cascade')
    room_id = fields.Many2one('alojamiento.rooms', string="Habitación", required=True, ondelete='cascade')
    student_id = fields.Many2one('alojamiento.students', string="Estudiante", required=True, ondelete='cascade')
    #assigned_date = fields.Date(default=fields.Date.today)
    type = fields.Selection([('AUT', 'Automática'), ('MAN', 'Manual')], string="Tipo")


    _sql_constraints = [
    ('booking_room_uniq', 'unique(room_id,booking_id)', 'La combinación de reserva y habitación debe ser único'),
    ]


    
    
    @api.model_create_multi #porque pueden haber variso registros de asignaciones
    def create(self, vals_list):  #create--> para que se ejecute cuando se crea un registro
        records = super().create(vals_list)
        template = self.env.ref(
            'alojamiento.email_template_assignment_confirmation',
            raise_if_not_found=False
        )
        if not template:
            return records

       
        for assigments in records:
            template.send_mail(assigments.id, force_send=True)
           
        return records 