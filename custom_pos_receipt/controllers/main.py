from odoo import http
from odoo.http import request
from datetime import datetime

class OptometristController(http.Controller):

    @http.route('/api/optometrist/assessment', type='json', auth='none', methods=['POST'])
    def create_optometrist_assessment(self, **kw):
        try:
            data = request.get_json_data()
            if not data:
                return {'error': 'Invalid JSON or empty request body'}, 400

            # Convert timestamps from milliseconds to seconds
            encounter_datetime = data.get('encounterDateTime')
            if encounter_datetime:
                encounter_datetime = datetime.fromtimestamp(int(encounter_datetime) / 1000)

            assessment = request.env['optometrist.assessment'].sudo().create({
                'encounter_uuid': data.get('encounterUuid'),
                'visit_uuid': data.get('visitUuid'),
                'patient_id': data.get('patientId'),
                'encounter_datetime': encounter_datetime,
                'observations': [(0, 0, {
                    'concept_uuid': obs.get('concept', {}).get('uuid'),
                    'concept_name': obs.get('concept', {}).get('name'),
                    'data_type': obs.get('concept', {}).get('dataType'),
                    'observation_uuid': obs.get('uuid'),
                    'value': obs.get('value'),
                    'observation_datetime': datetime.fromtimestamp(int(obs.get('observationDateTime')) / 1000) if obs.get('observationDateTime') else None,
                    'voided': obs.get('voided'),
                    'inactive': obs.get('inactive'),
                    'comment': obs.get('comment'),
                    'form_namespace': obs.get('formNamespace'),
                    'form_field_path': obs.get('formFieldPath'),
                    'group_members': obs.get('groupMembers'),
                    'interpretation': obs.get('interpretation'),
                }) for obs in data.get('observations', [])]
            })

            if hasattr(assessment, 'create_sale_order'):
                assessment.create_sale_order()

            return {'message': 'Assessment created successfully'}

        except Exception as e:
            return {'error': str(e)}, 500
