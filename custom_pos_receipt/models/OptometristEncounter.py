from odoo import models, fields

class OptometristEncounter(models.Model):
    _name = 'optometrist.encounter'
    _description = 'Optometrist Encounter'

    encounter_uuid = fields.Char(string='Encounter UUID')
    visit_uuid = fields.Char(string='Visit UUID')
    patient_id = fields.Char(string='Patient ID')
    patient_name = fields.Char(string='Patient Name')
    encounter_datetime = fields.Datetime(string='Encounter Date Time')
    observations = fields.One2many('optometrist.observation', 'assessment_id', string='Observations')
    sale_order = fields.Many2one('sale.order', string='Sale Order')

    def create_sale_order(self):
        """Creates a sale order with each observation as an item."""
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        Product = self.env['product.product']
        Partner = self.env['res.partner']
        Company = self.env['res.company']
        
        Shop = self.env['sale.shop']
        
        shop = Shop.search([], limit=1)

        # Find the patient in res.partner
        patient = Partner.search([('ref', '=', self.patient_id)], limit=1)
        if not patient:
            raise ValueError("Patient not found in system")
        
        # Find the company
        # Assuming the company is the first one in the list
        company = self.env.company or Company.search([], limit=1)

        # Create sale order
        sale_order = SaleOrder.create({
            'partner_id': patient.id,
            'date_order': self.encounter_datetime or fields.Datetime.now(),
            'origin': f'Encounter {self.encounter_uuid}',
            'company_id': company.id,
            'shop_id': shop.id,
        })

        # Add observations as sale order lines
        for observation in self.observations:
            product = Product.search([('name', '=', observation.concept_name)], limit=1)
            if not product:
                # Create the product if it doesn't exist
                product = Product.create({
                    'name': observation.concept_name,
                    'type': 'service',
                    'list_price': 0.0,  # Default price if not specified
                })

            # Add product to sale order line
            SaleOrderLine.create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': product.name,
                'product_uom_qty': 1,
                'price_unit': product.list_price,
            })
        
        self.patient_name = patient.name
        self.sale_order = sale_order.id
        self.write({
            'patient_name': patient.name,
            'sale_order': sale_order.id,
        })

        return sale_order

