from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

import re



class MaintenanceIssues(models.Model):
    _name = 'alojamiento.maintenanceissues'
    _description = 'Define cada las incidencias asociadas a los alojameintos'

    name = fields.Char(string="Identificador incidencia", size = 10, required = True)
    start_date= fields.Date(string="Fecha de alta", default=lambda self: date.today())
    end_date= fields.Date(string="Fecha de baja", readonly=True)
    status = fields.Selection([('PEN','Pendiente'),('PRO','En proceso'),('RES', 'Resuelta')])
    description = fields.Text(string="Descripción incidencia")

    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]

 # Maintenanceissues [1]:[N] Accommodations
    accommodation_id = fields.Many2one('alojamiento.accommodations')
    
#poner un identificador automático
    @api.constrains('name')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("\d{3,}")
            if not pattern.match(record.name):
                raise ValidationError('El formato deben ser NNN donde N un número')

#regsitra la fecha de baja cuando cambia el status

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'RES'and self.end_date == False:
            self.end_date = date.today()