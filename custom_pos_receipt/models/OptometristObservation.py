from odoo import models, fields


class OptometristObservation(models.Model):
    _name = 'optometrist.observation'
    _description = 'Optometrist Observation'

    assessment_id = fields.Many2one('optometrist.encounter', string='Optometrist Assessment')
    concept_uuid = fields.Char(string='Concept UUID')
    concept_name = fields.Char(string='Concept Name')
    data_type = fields.Char(string='Data Type')
    observation_uuid = fields.Char(string='Observation UUID')
    value = fields.Char(string='Value')
    observation_datetime = fields.Datetime(string='Observation Datetime')
    voided = fields.Boolean(string='Voided')
    inactive = fields.Boolean(string='Inactive')
    comment = fields.Text(string='Comment')
    form_namespace = fields.Char(string='Form Namespace')
    form_field_path = fields.Char(string='Form Field Path')
    group_members = fields.Char(string='Group Members')
    interpretation = fields.Char(string='Interpretation')
