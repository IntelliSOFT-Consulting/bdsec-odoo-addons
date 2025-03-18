from odoo import http
import json

class OptometristController(http.Controller):

    @http.route('/api/optometrist/assessment', type='json', auth='none', methods=['POST'])
    def create_optometrist_assessment(self, **kw):
        data = kw.get('data')
        assessment = http.request.env['optometrist.assessment'].create({
            'encounter_uuid': data.get('encounterUuid'),
            'visit_uuid': data.get('visitUuid'),
            'patient_id': data.get('patientId'),
            'encounter_datetime': data.get('encounterDateTime'),
            'observations': [(0, 0, {
                'concept_uuid': obs.get('concept').get('uuid'),
                'concept_name': obs.get('concept').get('name'),
                'data_type': obs.get('concept').get('dataType'),
                'observation_uuid': obs.get('uuid'),
                'value': obs.get('value'),
                'observation_datetime': obs.get('observationDateTime'),
                'voided': obs.get('voided'),
                'inactive': obs.get('inactive'),
                'comment': obs.get('comment'),
                'form_namespace': obs.get('formNamespace'),
                'form_field_path': obs.get('formFieldPath'),
                'group_members': obs.get('groupMembers'),
                'interpretation': obs.get('interpretation'),
            }) for obs in data.get('observations')]
        })
        assessment.create_sale_order()
        return {'message': 'Assessment created successfully'}
