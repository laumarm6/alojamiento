from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Contracts(models.Model):
    _name = 'alojamiento.contracts'
    _description = 'Define cada uno de los alojamientos para estudiantes'

    name = fields.Char(string="Identificador contrato", size = 10, required = True)
    status = fields.Boolean()
    start_date = fields.Date(string = 'Fecha de alta')
    end_date =fields.Date(string = 'Fecha de baja')
    #me falta el campo de subir archivo y poder previsualizarlo


    _sql_constraints = [
    ('name_uniq', 'unique(name)', 'El identificador debe ser único'),
]
    
# Contracts [N]:[1] Landlords
    landlord_id = fields.Many2one('alojamiento.landlords')




    @api.constrains('name')
    def _check_identificador(self):
        for record in self:
            pattern = re.compile("^[A-Z]{3}\d{5,}$")
            if not pattern.match(record.name):
                raise ValidationError('El formato deben ser AAANNNNN donde A es una letra mayúscula y N un número')
        