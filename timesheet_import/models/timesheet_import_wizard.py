from odoo import models, fields, api, _
from datetime import datetime
import base64
import csv
import io
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class TimesheetImportWizard(models.TransientModel):
    _name = 'timesheet.import.wizard'
    _description = 'Import Timesheet Wizard'

    month = fields.Selection(
        selection=[
            ('01', 'January'),
            ('02', 'February'),
            ('03', 'March'),
            ('04', 'April'),
            ('05', 'May'),
            ('06', 'June'),
            ('07', 'July'),
            ('08', 'August'),
            ('09', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December')
        ],
        string='Month',
        default=lambda self: datetime.now().strftime('%m'),
        required=True
    )

    year = fields.Selection(
        selection='_get_year_selection',
        string='Year',
        default=lambda self: datetime.now().strftime('%Y'),
        required=True
    )

    file = fields.Binary('File', required=True, help="Upload the CSV file for timesheets")
    file_name = fields.Char(string='Filename')

    @api.model
    def _get_year_selection(self):
        current_year = int(datetime.now().strftime('%Y'))
        return [(str(year), str(year)) for year in range(current_year - 5, current_year + 5)]

    def import_timesheet(self):
        if not self.file:
            raise ValidationError(_('No file uploaded. Please upload a valid CSV file.'))

        try:
            data = base64.b64decode(self.file)
            file_content = io.StringIO(data.decode('utf-8'))
            csv_reader = csv.reader(file_content, delimiter=',')
            
            # Skip the first 4 rows
            for _ in range(4):
                next(csv_reader)

            # The fifth row contains the days of the month
            days_row = next(csv_reader)
            days_of_month = [int(day.strip()) for day in days_row[1:] if day.strip().isdigit()]
        except Exception as e:
            raise ValidationError(_('Unable to read the uploaded file. Please ensure it is a valid CSV.'))

        user_employee = self.env.user.employee_id
        if not user_employee:
            raise ValidationError(_('The current user is not associated with any employee.'))

        _logger.info("Logged-in User: %s, Employee ID: %s", self.env.user.name, user_employee.id)

        for index, row in enumerate(csv_reader, start=1):
            try:
                category = row[0].strip()
                if not category:
                    _logger.warning("Skipping empty row at line %d", index)
                    continue

                for day, value in zip(days_of_month, row[1:]):
                    if not value.strip().isdigit():
                        continue

                    hours = float(value.strip())
                    date = datetime(int(self.year), int(self.month), day)

                    task_name = category + " Task"
                    task = self.env['project.task'].search([('name', '=', task_name)], limit=1)
                    if not task:
                        task = self.env['project.task'].create({
                            'name': task_name,
                            'project_id': self.env['project.project'].search([], limit=1).id,
                        })

                    account_id = task.analytic_account_id.id if task.analytic_account_id else None
                    if not account_id:
                        raise ValidationError(_('No analytic account set for task "%s".') % task_name)

                    self.env['account.analytic.line'].create({
                        'date': date,
                        'name': category,
                        'unit_amount': hours,
                        'employee_id': user_employee.id,
                        'task_id': task.id,
                        'account_id': account_id,
                    })

                    _logger.info("Timesheet entry created for employee %s on task %s for date %s.", user_employee.name, task.name, date)

            except Exception as e:
                _logger.error("Error on line %d: %s", index, str(e))
                raise ValidationError(_('Error on line %d: %s') % (index, str(e)))

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
