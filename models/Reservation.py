from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Reservation(models.Model):
    _name = 'reservation'
    _description = 'Reservation Description'

    client_id = fields.Many2one('client', string="Client", required=True)

    startfrom = fields.Date(default=fields.Datetime.now, string='Starting from', required=True)
    end = fields.Date(default=fields.Datetime.now,string='Ending at', required=True)

    brandavailable = fields.Selection(selection='_get_brands', string="Brand Chosen", required=True)
    caravailable = fields.Selection(selection='_get_names', string="Car Chosen", required=True)
    matriculeavailable = fields.Selection(selection='_get_matricules', string="Matricule Chosen", required=True)

    priceperday = fields.Float(string="Price per Day", required=True)
    days = fields.Integer(string="Number of days", compute='_compute_days', store=True)
    Total = fields.Float(string="Total", compute='_compute_total', store=True)

    @api.depends('startfrom', 'end')
    def _compute_days(self):
        for record in self:
            if record.startfrom and record.end:
                start_date = fields.Date.from_string(record.startfrom)
                end_date = fields.Date.from_string(record.end)
                if end_date > start_date:
                    delta = end_date - start_date
                    record.days = delta.days + 1
                else:
                    record.days = 0
            else:
                record.days = 0

    @api.depends('days', 'priceperday')
    def _compute_total(self):
        for record in self:
            record.Total = record.days * record.priceperday

    @api.onchange('startfrom', 'end', 'priceperday')
    def _onchange_dates_price(self):
        for record in self:
            if record.startfrom and record.end and record.startfrom <= record.end:
                start_date = fields.Date.from_string(record.startfrom)
                end_date = fields.Date.from_string(record.end)
                delta = end_date - start_date
                record.days = delta.days + 1
                record.Total = record.days * record.priceperday
            else:
                record.days = 0
                record.Total = 0

    @api.model
    def _get_brands(self):
        cars = self.env['car'].search([])
        unique_brands = set(car.brandcar for car in cars)
        return [(brand, brand) for brand in unique_brands]

    @api.model
    def _get_matricules(self):
        cars = self.env['car'].search([])
        return [(car.matricule, car.matricule) for car in cars]

    @api.model
    def _get_names(self):
        cars = self.env['car'].search([])
        return [(car.namecar, car.namecar) for car in cars]

    @api.constrains('priceperday')
    def _check_price_greater_zero(self):
        for rec in self:
            if rec.priceperday == 0:
                raise ValidationError("Please add the price per day")

    @api.constrains('days')
    def _check_days_greater_zero(self):
        for rec in self:
            if rec.days == 0:
                raise ValidationError("Please check the dates you selected !")

    @api.constrains('caravailable', 'matriculeavailable', 'brandavailable', 'startfrom', 'end')
    def _check_car_and_its_availability(self):
        for rec in self:
            m = rec.matriculeavailable
            b = rec.brandavailable
            n = rec.caravailable
            s = fields.Date.from_string(rec.startfrom)
            e = fields.Date.from_string(rec.end)
            car = self.env['car'].search([('matricule', '=', m), ('brandcar', '=', b), ('namecar', '=', n)])
            if car:
                reservations = self.env['reservation'].search([
                    ('matriculeavailable', '=', m),
                    '|',
                    '&', ('startfrom', '<=', s), ('end', '>=', s),
                    '&', ('startfrom', '<=', e), ('end', '>=', e),
                    '&', ('startfrom', '>=', s), ('end', '<=', e),
                ])
                reservations -= rec
                if reservations:
                    raise ValidationError("Car is not available for the specified period.")
            else:
                raise ValidationError("Check the car's details there's a problem !")

    @api.model
    def create(self, vals):
        reservation = super(Reservation, self).create(vals)
        reservation.update_car_state()
        return reservation

    @api.model
    def update(self, vals):
        reservation = super(Reservation, self).write(vals)
        reservation.update_car_state()
        return reservation

    @api.model
    def write(self, vals):
        res = super(Reservation, self).write(vals)
        self.update_car_state()
        return res

    @api.model
    def unlink(self):
        res = super(Reservation, self).unlink()
        self.update_car_state()
        return res

    @api.model
    def update_car_state(self):
        today = fields.Date.today()
        model = self.env['car'].search([])
        for reservation in self:
            cars = model.search([('matricule', '=', reservation.matriculeavailable)])
            for car in cars:
                carRented = self.env['reservation'].search(
                    [('matriculeavailable', '=', car.matricule), ('startfrom', '<', today), ('end', '>', today)])
                carTodayBack = self.env['reservation'].search(
                    [('matriculeavailable', '=', car.matricule), ('startfrom', '<=', today), ('end', '=', today)])
                carTodayRent = self.env['reservation'].search(
                    [('matriculeavailable', '=', car.matricule), ('startfrom', '=', today), ('end', '>=', today)])
                if carRented:
                    car.write({'state': "rented"})
                else:
                    if carTodayRent:
                        if carTodayBack:
                            car.write({'state': "rent_back_today"})
                        else:
                            car.write({'state': "rent_today"})
                    else:
                        if carTodayBack:
                            car.write({'state': "rent_today"})
                        else:
                            car.write({'state': "available"})