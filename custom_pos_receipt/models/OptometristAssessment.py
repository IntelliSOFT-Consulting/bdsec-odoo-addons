from odoo import models, fields

class OptometristAssessment(models.Model):
    _name = 'optometrist.assessment'
    _description = 'Optometrist Assessment'

    encounter_uuid = fields.Char(string='Encounter UUID')
    visit_uuid = fields.Char(string='Visit UUID')
    patient_id = fields.Char(string='Patient ID')
    encounter_datetime = fields.Datetime(string='Encounter Datetime')
    observations = fields.One2many('optometrist.observation', 'assessment_id', string='Observations')
    
    
    def create_sale_order(self):
        """Creates a sale order with each observation as an item."""
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        Product = self.env['product.product']
        Partner = self.env['res.partner']

        # Find the patient in res.partner
        patient = Partner.search([('id', '=', self.patient_id)], limit=1)
        if not patient:
            raise ValueError("Patient not found in system")

        # Create sale order
        sale_order = SaleOrder.create({
            'partner_id': patient.id,
            'date_order': self.encounter_datetime or fields.Datetime.now(),
            'origin': f'Encounter {self.encounter_uuid}',
        })

        # Add observations as sale order lines
        for observation in self.observations:
            product = Product.search([('name', '=', observation.name)], limit=1)
            if not product:
                # Create the product if it doesn't exist
                product = Product.create({
                    'name': observation.name,
                    'type': 'service',
                    'list_price': observation.price or 0.0,  # Default price if not specified
                })

            # Add product to sale order line
            SaleOrderLine.create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': product.name,
                'product_uom_qty': 1,
                'price_unit': product.list_price,
            })

        return sale_order
