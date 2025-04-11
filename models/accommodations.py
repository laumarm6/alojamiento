from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Accommodations(models.Model):
    _name = 'alojamiento.accommodations'
    _description = 'Define cada uno de los alojamientos'

    code = fields.Char(string="Identificador alojamiento", size = 10, required = True)
    name = fields.Char(string = "Nombre", required = True)
    address = fields.Text(string = "Dirección", required=True)
    type = fields.Selection([('APT','Apartamento'),('RES','Residencia'),('FAM', 'Familia')], required=True)
    status = fields.Boolean()

    _sql_constraints = [
    ('code_uniq', 'unique(code)', 'El identificador debe ser único'),
    ('name_uniq', 'unique(name)', 'El nombre debe ser único'),
     ]
    
    #poner un identificador automático
    @api.constrains('code')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("^[A-Z]{3}\d{5,}$")
            if not pattern.match(record.code):
                raise ValidationError('El formato deben ser AAANNNNN donde A es una letra mayúscula y N un número')
    