from odoo import models, fields


class MaintenanceIssues(models.Model):
    _name = 'alojamiento.maintenanceissues'
    _description = 'Define cada las incidencias asociadas a los alojameintos'

    name = fields.Char(string="Nombre")
    status = fields.Char()