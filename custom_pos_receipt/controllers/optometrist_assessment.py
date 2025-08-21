from odoo import http
from odoo.http import Response, request
import json
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class OptometristController(http.Controller):

    @http.route('/api/optometrist/assessment', type='http', auth='none', methods=['POST'], csrf=False)
    def create_optometrist_assessment(self, **kwargs):
        try:
            data = request.get_json_data()
            # _logger.info("Received data for optometrist assessment: %s", json.dumps(data))


            if not data.get('observations') or not data:
                return Response(json.dumps({
                    'error': 'Missing required fields',
                    'status': 'error'
                }), status=400, content_type='application/json')
            

            assessment = http.request.env['optometrist.encounter'].sudo().create({
                'encounter_uuid': data.get('encounterUuid'),
                'visit_uuid': data.get('visitUuid'),
                'patient_id': data.get('patientId'),
                # 'encounter_datetime': data.get('encounterDateTime'),
                'encounter_datetime': datetime.fromtimestamp(int(data.get('encounterDateTime')) / 1000.0),
                'observations': [(0, 0, {
                    'concept_uuid': obs.get('concept', {}).get('uuid'),
                    'concept_name': obs.get('concept', {}).get('name'),
                    'data_type': obs.get('concept', {}).get('dataType'),
                    'observation_uuid': obs.get('uuid'),
                    'value': (
                        obs.get('valueAsString') or
                        (obs.get('value', {}).get('name') if isinstance(obs.get('value'), dict) else obs.get('value'))
                    ),
                    'observation_datetime': datetime.fromtimestamp(int(obs.get('observationDateTime')) / 1000.0) if obs.get('observationDateTime') else None,
                    'voided': obs.get('voided'),
                    'inactive': obs.get('inactive'),
                    'comment': obs.get('comment'),
                    'form_namespace': obs.get('formNamespace'),
                    'form_field_path': obs.get('formFieldPath'),
                    'group_members': obs.get('groupMembers'),
                    'interpretation': obs.get('interpretation'),
                }) for obs in data.get('observations', [])]

            })

            # Optional: handle logic that might also throw errors
            try:
                assessment.create_sale_order()
            except Exception as e:
                _logger.error("Error creating sale order: %s", str(e))
                return Response(json.dumps({
                    'error': 'Assessment created but sale order failed',
                    'details': str(e),
                    'status': 'error'
                }), status=500, content_type='application/json')

            return Response(json.dumps({
                'message': 'Assessment created successfully',
                'id': assessment.id,
                'status': 'success'
            }), status=201, content_type='application/json')

        except Exception as e:
            _logger.error("Error creating optometrist assessment: %s", str(e), exc_info=True)
            return Response(json.dumps({
                'error': 'Failed to create assessment',
                'details': str(e),
                'status':'error'
            }), status=500, content_type='application/json')
