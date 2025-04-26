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
    asigment_state = fields.Selection([('PND', 'Pendiente'), ('ASG', 'Asignada'), ('SDP', 'Sin Disponibilidad')], default='PND')
    days = fields.Integer(string="Duración", compute='_compute_days')
    


    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]
    
    # Bookings [N]:[1] Clients
    client_id = fields.Many2one('alojamiento.aclients', string = "Cliente")

    # Bookings [N]:[N] Estudiantes
    students_ids = fields.Many2many('alojamiento.students', string = "Estudiantes")

    # Bookings [N]:[N] Habitaciones
    assigments_ids = fields.One2many('alojamiento.booking_room_rel','booking_id', string = "Habitaciones asignadas")
    

    students_names = fields.Char(string="Nombres estudiantes", compute='_compute_students_names')
    
    
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

    @api.depends('students_ids')
    def _compute_students_names(self):
        for record in self:
            student_names = [student.name for student in record.students_ids]
            record.students_names = '/ '.join(student_names)


    @api.model
    def assign_rooms(self):
        # Buscar reservas pendientes sin asignación
        pending = self.search([('status', '=', 'PEN'), ('assigments_ids', '=', False)])
        for res in pending:
            # nivel del estudiante (tomamos el primero si hay varios)
            level = res.students_ids and res.students_ids[0].level or False
            # Buscar habitaciones libres de mismo tipo y nivel
            rooms = self.env['alojamiento.rooms'].search([
                ('is_occupied', False),
                ('accommodation_id.type', '=', res.type),
                ('level', '=', level),
            ])
            # Si no hay buscar habitación libre del tipo ordenado por distancia
            if not rooms:
                rooms = self.env['alojamiento.rooms'].search([
                    ('is_occupied', False),
                    ('accommodation_id.type', '=', res.type),
                ], order='accommodation_id.distance')

            # Si no hay habitaciones disponibles marcar 'sin disponibilidad'
            if not rooms:
                res.status = 'SIN'
                continue

            # Asignar la primera habitación
            room = rooms[0]
            rec = self.env['alojamiento.booking_room_rel'].create({
                'booking_id': res.id,
                'room_id':    room.id,
            })
            room.is_occupied = True
            res.status = 'ASN'
            # Enviar email 
            template = self.env.ref('alojamiento.email_template_reservation_confirmation')
            template.send_mail(res.id, force_send=True)
        return True
