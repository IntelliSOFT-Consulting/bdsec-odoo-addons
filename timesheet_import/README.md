# odoo-custom-timesheet import
<!-- Documentstion guide -->
Create a csv timesheet for importation

Available fields on the timesheet.

self.env['account.analytic.line'].create({
    'name': 'Development Work on Project XYZ',
    'date': '2024-11-28',
    'unit_amount': 6.0,  # hours worked
    'product_id': product_id,  # Optional: Linked product
    'project_id': project_id,  # Optional: Associated project
    'task_id': task_id,  # Associated task
    'account_id': analytic_account_id,  # Optional: Analytic account
    'user_id': user_id,  # User who logged the timesheet
})


/home/wahome/Downloads/Analytic Line (account.analytic.line) (3).csv