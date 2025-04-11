from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re


class MaintenanceIssues(models.Model):
    _name = 'alojamiento.maintenanceissues'
    _description = 'Define cada las incidencias asociadas a los alojameintos'

    name = fields.Char(string="Identificador incidencia", size = 10, required = True)
    status = fields.Selection([('PEN','Pendiente'),('PRO','En proceso'),('RES', 'Resuelta')])


    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]

#poner un identificador automático
    @api.constrains('name')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("\d{3,}")
            if not pattern.match(record.name):
                raise ValidationError('El formato deben ser NNN donde N un número')
        