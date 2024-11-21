from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _get_report_template_id(self):
        return self.env.ref('custom_pos_receipt.report_invoice_pos_custom')