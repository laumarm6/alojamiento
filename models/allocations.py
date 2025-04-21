from odoo import models, fields


class Allocations(models.Model):
    _name = 'alojamiento.allocations'
    _description = 'Relación entre reservas, estudiantes y habitaciones asignadas'

    name = fields.Char(string="Identificador")
    type = fields.Selection([('AUT', 'Automática'), ('MAN', 'Manual')])
    

    
    
   