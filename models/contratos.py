from odoo import models, fields


class Contratos(models.Model):
    _name = 'alojamiento.contratos'
    _description = 'Define cada uno de los alojamientos para estudiantes'

    idContrato = fields.Char(string='Codigo del contrato')
    idPropietario = fields.Many2one('alojamiento.propietarios', string='Propietario')
    archivo_adjunto = fields.Binary(string='Doc Contrato', attachment=True)
    archivo_nombre = fields.Char(string='Nombre del Archivo')
    status = fields.Char()

    