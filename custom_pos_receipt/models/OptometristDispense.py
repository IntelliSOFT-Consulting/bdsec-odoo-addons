from odoo import models, fields

class OptometristDispense(models.Model):
    _name = 'optometrist.dispense'
    _description = 'Optometrist Dispense'
    
    optometrist_encounter = fields.Many2one(
        'optometrist.encounter',
        string="Optometrist Encounter",
        required=True,
        ondelete='cascade',
        help="The encounter associated with this dispense record.")

    # Frame Info
    brand = fields.Selection([
        ('ray_ban', 'Ray Ban'), ('tomford', 'Tomford'), ('gucci', 'Gucci'),
        ('channel', 'Channel'), ('cartier', 'Cartier'), ('prada', 'Prada'),
        ('pardasul', 'Pardasul'), ('dakley', 'Dakley'), ('boss', 'Boss'),
        ('hugo_boss', 'Hugo Boss'), ('dior', 'Dior'), ('tommy', 'Tommy'),
        ('cooking', 'Cooking'), ('calvin_clain', 'Calvin Clain'),
        ('police', 'Police'), ('dg', 'D&G'), ('burberry', 'Burberry'),
        ('terios', 'Terios'), ('others', 'Others')
    ], string="Brand")

    model = fields.Char(string="Model")
    eye_size = fields.Char(string="Eye Size")
    bridge_size = fields.Char(string="Bridge Size")
    temple_length = fields.Char(string="Temple Length")

    frame_material = fields.Selection([
        ('titanium', 'Titanium'), ('aluminum', 'Aluminum'), ('metal', 'Metal'),
        ('bronze', 'Bronze'), ('stainless_steel', 'Stainless Steel'), ('monel', 'Monel'),
        ('cellulose_acetate', 'Cellulose Acetate'), ('propionate', 'Propionate'),
        ('nylon', 'Nylon'), ('tr90', 'TR90'), ('optyl', 'Optyl'),
        ('wood', 'Wood'), ('carbon_fiber', 'Carbon Fiber'),
        ('buffalo_horn', 'Buffalo Horn'), ('leather', 'Leather')
    ], string="Frame Material")

    frame_mounting = fields.Selection([
        ('full_rim', 'Full rim'), ('half_rim', 'Half rim'),
        ('rimless', 'Rimless'), ('hybrid', 'Hybrid')
    ], string="Frame Mounting")

    patient_buy = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Patient Decided to Buy?")
    buy_type = fields.Selection([('custom', 'Custom Made'), ('readymade', 'Readymade'), ('ready_to_clip', 'Ready to Clip')], string="If Yes - Type")
    power = fields.Char(string="Power (if readymade/clip)")
    refusal_reason = fields.Text(string="If No - Reason")

    frame_price = fields.Float(string="Frame Price (Custom Made)")
    lens_price = fields.Float(string="Lens Price (Custom Made)")
    total_price = fields.Float(string="Total Price")
    initial_payment = fields.Float(string="Initial Payment (70%)")

    payment_method = fields.Selection([
        ('cash', 'Cash'), ('credit', 'Credit'),
        ('insurance', 'Insurance'), ('other', 'Other')
    ], string="Payment Method")

    insurance_provider = fields.Char(string="Insurance Provider")
    coverage_details = fields.Text(string="Coverage Details")
    out_of_pocket = fields.Float(string="Patient Out-of-Pocket")

    bifocal_segment_height = fields.Char(string="Bifocal Segment Height")
    progressive_height = fields.Char(string="Progressive Fitting Cross Height")
    pupillary_height = fields.Char(string="Pupillary Height (Single Vision)")

    # Order Details
    order_date = fields.Date(string="Order Date")
    order_number = fields.Char(string="Order Number")
    available_in_stock = fields.Boolean(string="Available in Stock?")
    delivery_date = fields.Date(string="Delivery Date")
    adjustment_made = fields.Boolean(string="Adjustments Made at Dispensing")
    adjustment_note = fields.Text(string="Adjustment Note")

    # Glazing
    quality_check = fields.Boolean(string="Quality Check Performed?")
    issues_noted = fields.Boolean(string="Issues Noted?")
    issue_type = fields.Selection([
        ('power_variation', 'Power Variation'),
        ('incorrect_pd', 'Incorrect PD'),
        ('stress_marks', 'Stress Marks'),
        ('chipping', 'Chipping'),
        ('misalignment', 'Misalignment'),
        ('bubbles', 'Bubbles'),
        ('other', 'Other')
    ], string="Issue Type")
    issue_other = fields.Char(string="Other Issue Description")
    resolving_done = fields.Text(string="Resolving Done")

    # Collection
    care_instructions = fields.Boolean(string="Care Instructions Provided?")
    warranties = fields.Boolean(string="Warranties Explained?")
    return_policy = fields.Boolean(string="Return Policy Explained?")
