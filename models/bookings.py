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
    asigment_state = fields.Selection([('PND', 'Pendiente'), ('ASN', 'Asignada'), ('SIN', 'Sin Disponibilidad')], default='PND')
    days = fields.Integer(string="Duración", compute='_compute_days')
    type = fields.Selection([('APT','Apartamento'),('RES','Residencia'),('FAM', 'Familia')], required=True)
    


    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]
    
    # Bookings [N]:[1] Clients
    client_id = fields.Many2one('alojamiento.aclients', string = "Cliente")

    # Bookings [N]:[N] Estudiantes
    students_ids = fields.Many2many('alojamiento.students', string = "Estudiantes")

    # Bookings [N]:[N] Habitaciones
    assigments_ids = fields.One2many('alojamiento.booking_room_rel','booking_id', string = "Habitaciones asignadas")
    

    students_names = fields.Char(string="Nombres estudiantes", compute='_compute_students_names', store=True)
    
    
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


    #
    def assign_single_booking(self):
        self.ensure_one()

        #if self.status != 'PEN' or self.assigments_ids:
        if self.asigment_state != 'PEN' or self.status != 'CONF' or self.assigments_ids:
            return

        # Nivel del estudiante (asumimos que todos los estudiantes tienen el mismo nivel)
        level = self.students_ids and self.students_ids[0].level or False

        # Buscar alojamientos del tipo necesario
        accommodations = self.env['alojamiento.accommodations'].search([('type', '=', self.type)])
        accommodation_ids = accommodations.ids

        # Buscar habitaciones libres de mismo tipo y nivel
        rooms = self.env['alojamiento.rooms'].search([
            ('is_occupied', '=', False),
            ('accommodation_id', 'in', accommodation_ids),
        ])

        if not rooms:
            rooms = self.env['alojamiento.rooms'].search([
                ('is_occupied', '=', False),
                ('accommodation_id', 'in', accommodation_ids),
            ], order='accommodation_id.distance')

        if not rooms:
            self.asigment_state = 'SIN'
            return

        # Comprobar si ya hay estudiantes asignados en las mismas fechas
        for room in rooms:
            # Comprobamos si hay estudiantes asignados en las fechas solicitadas
            existing_assignments = self.env['alojamiento.booking_room_rel'].search([
                ('room_id', '=', room.id),
                ('booking_id', '!=', self.id),  # Excluir la propia reserva
                ('booking_id.start_date', '<', self.end_date),
                ('booking_id.end_date', '>', self.start_date),  # Asegurarse de que las fechas se solapan
            ])

            if existing_assignments:
                # Si hay asignaciones existentes, seguimos buscando
                continue

            # Asignar la habitación disponible
            self.env['alojamiento.booking_room_rel'].create({
                'booking_id': self.id,
                'room_id': room.id,
            })
            room.is_occupied = True
            self.asigment_state = 'ASN'

            # Enviar email de confirmación
            #template = self.env.ref('alojamiento.email_template_reservation_confirmation', raise_if_not_found=False)
            #if template:
            #    template.send_mail(self.id, force_send=True)

            break
        else:
            # Si no se asignaron habitaciones, cambiar estado de asignación
            self.asigment_state = 'SIN'

        # Enviar email de confirmación
        #template = self.env.ref('alojamiento.email_template_reservation_confirmation', raise_if_not_found=False)
        #if template:
           # template.send_mail(self.id, force_send=True)