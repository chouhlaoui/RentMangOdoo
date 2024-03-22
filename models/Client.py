from odoo import models, fields

class Client(models.Model):

    _name ='client'
    _description = 'Client Description'
    _rec_name = 'identity'

    _log_access = False

    fullname = fields.Char(string="Full Name", required=True)
    nationality = fields.Char(string="Nationality")
    identity = fields.Char(string="Identity", required=True)
    dateidentity = fields.Date(string="Identity Date", required=True)
    drivinglicence = fields.Char(string="Driving Licence", required=True)
    datelicence = fields.Date(string="Licence Date", required=True)
    address = fields.Char(string="Address")
    phonenumber = fields.Integer(string="Phone Number", required=True)

    reservations_ids = fields.One2many('reservation', 'client_id')

    _sql_constraints = [
        ('unique_client', 'unique("identity")', 'This Client exists!')
    ]

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.identity, rec.identity))
        return result
