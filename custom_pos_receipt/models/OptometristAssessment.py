from odoo import models, fields

class OptometristAssessment(models.Model):
    _name = 'optometrist.assessment'
    _description = 'Optometrist Assessment'

    encounter_uuid = fields.Char(string='Encounter UUID')
    visit_uuid = fields.Char(string='Visit UUID')
    patient_id = fields.Char(string='Patient ID')
    encounter_datetime = fields.Datetime(string='Encounter Datetime')
    observations = fields.One2many('optometrist.observation', 'assessment_id', string='Observations')
