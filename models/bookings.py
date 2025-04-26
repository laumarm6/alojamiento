from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Bookings(models.Model):
    _name = 'alojamiento.bookings'
    _description = 'Registra las reservas hechas'

    name = fields.Char(string="Identificador", required=True)
    start_date= fields.Date(string="Fecha inicio", required=True)
    end_date= fields.Date(string="Fecha fin", required=True)
    status = fields.Selection([('PEN', 'Pendiente'), ('CONF', 'Confirmada'), ('CANC', 'Cancelada')], default='PEN', string = "Estado reserva")
    asigment_state = fields.Selection([('PND', 'Pendiente'), ('ASN', 'Asignada'), ('SIN', 'Sin Disponibilidad')], default='PND', string = "Estado asignación")
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
    

#####asignacion 1 hab+recorrer studnets reserva
    
    def assign_bookings(self):
        self.ensure_one()
        # Sólo asigna si la reserva está confirmada y aún sin asignar
        if self.asigment_state != 'PND' or self.status != 'CONF' or self.assigments_ids:
            return

        # Recogemos recordset con todos los estudiantes de esta reserva
        students_to_assign = self.students_ids[:]  

        # Preparamos lista de alojamientos válidos
        accommodations = self.env['alojamiento.accommodations'].search([
            ('type', '=', self.type),
        ])
        accommodation_ids = accommodations.ids

        # Para cada estudiante de la reserva vamos a asiganr una habitación
        for student in students_to_assign:  
            

            # busco hab mismo tipo
            rooms = self.env['alojamiento.rooms'].search([
               # ('is_occupied', '=', False),
                ('accommodation_id', 'in', accommodation_ids),
                
            ])
            # Si no hay, busco por distancia
            if not rooms:
                rooms = self.env['alojamiento.rooms'].search([
                    #('is_occupied', '=', False),
                    ('accommodation_id', 'in', accommodation_ids),
                ])

            # Si aún no hay, marco sin disponibilidad y terminamos
            if not rooms:
                self.asigment_state = 'SIN'
                return
            #ordeno por distancia antes de asignar
            rooms = sorted(list(rooms), key=lambda room: room.accommodation_id.distance)
            
            # busco libre por fechas
            assigned = False
            for room in rooms:
                overlapping = self.env['alojamiento.booking_room_rel'].search([
                    ('room_id', '=', room.id),
                    ('booking_id.start_date', '<', self.end_date),
                    ('booking_id.end_date', '>', self.start_date),
                ])
                if overlapping:
                    continue
                # Creamos la relación reserva–habitación–estudiante
                self.env['alojamiento.booking_room_rel'].create({  
                    'booking_id': self.id,
                    'room_id':    room.id,
                    'student_id': student.id,                        
                })
                #room.is_occupied = True
                assigned = True
                break

            if not assigned:
                
                self.asigment_state = 'SIN'
                return

       
        self.asigment_state = 'ASN'
        # Enviar email de confirmación …
        # template = self.env.ref('alojamiento.email_template_reservation_confirmation', raise_if_not_found=False)
        # if template:
        #     template.send_mail(self.id, force_send=True)