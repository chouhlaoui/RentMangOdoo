from odoo import models,fields,api

class Car(models.Model):
    _name ='car'
    _description = 'Car Description'

    _log_access = False

    matricule = fields.Char(string="Matricule", required=True)
    namecar = fields.Char(string="Car Name", required=True)
    brandcar = fields.Char(string="Car Brand", required=True)

    state = fields.Selection([
        ('available', 'Available'),
        ('rent_today', 'Rent Today'),
        ('rented', 'Rented'),
        ('back_today', 'Back Today'),
        ('rent_back_today', 'Back then Rent Today'),
    ], default='available')

    _sql_constraints = [
        ('unique_matricule', 'unique("matricule")', 'This Car exists!')
    ]

    @api.model
    def create_car(self, vals):
        car = super(Car, self).create(vals)
        return car

    @api.model
    def update_car(self, car_data):
        self.write(car_data)
        return True

    @api.model
    def delete_car(self):
        self.unlink()
        return True

    def save_car(self):
        self.ensure_one()
        if self.id:
            self.update_car({
                    'matricule': self.matricule,
                    'namecar': self.namecar,
                    'brandcar': self.brandcar,
                })
        else:
            self.create_car({
                'matricule': self.matricule,
                'namecar': self.namecar,
                'brandcar': self.brandcar,
                'state': "available"
            })
