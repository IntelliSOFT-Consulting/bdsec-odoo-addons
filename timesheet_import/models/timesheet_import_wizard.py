from odoo import models, fields, api, _
import base64
import csv
import io
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class TimesheetImportWizard(models.TransientModel):
    _name = 'timesheet.import.wizard'
    _description = 'Import Timesheet Wizard'

    file = fields.Binary('File', required=True, help="Upload the CSV file for timesheets")
    file_name = fields.Char('File Name')

    def import_timesheet(self):
        for wizard in self:
            if not wizard.file:
                raise ValidationError(_('No file uploaded. Please upload a valid CSV file.'))

            try:
                data = base64.b64decode(wizard.file)
                file_content = io.StringIO(data.decode('utf-8'))
                csv_reader = csv.reader(file_content, delimiter=',')
                next(csv_reader)
            except Exception as e:
                raise ValidationError(_('Unable to read the uploaded file. Please ensure it is a valid CSV.'))

            user_employee = self.env.user.employee_id
            if not user_employee:
                user_details = {
                    'name': self.env.user.name,
                    'login': self.env.user.login,
                    'email': self.env.user.email,
                    'groups': ', '.join([group.name for group in self.env.user.groups_id]),
                }
                raise ValidationError(
                    _('The current user (%(name)s) with login %(login)s and email %(email)s is not associated with any employee. Groups: %(groups)s') % user_details
                )

            _logger.info("Logged-in User: %s, Employee ID: %s", self.env.user.name, user_employee.id)

            for index, row in enumerate(csv_reader, start=1):
                try:
                    if not row or all(field.strip() == '' for field in row):
                        _logger.warning("Skipping empty row at line %d", index)
                        continue
                    
                    if len(row) < 4:
                        raise ValidationError(_('Error on line %d: Missing or incomplete data. Expected 4 fields but got %d.') % (index, len(row)))

                    date_str, name, hours, task_name = row

                    _logger.info("Processing row %d: %s", index, row)

                    try:
                        date = fields.Date.from_string(date_str)
                    except ValueError:
                        raise ValidationError(_('Invalid date format at line %d. Ensure the date is in the correct format.') % index)

                    task = self.env['project.task'].search([('name', '=', task_name)], limit=1)
                    if not task:
                        _logger.info("Task with name '%s' does not exist. Creating a new task.", task_name)

                        task = self.env['project.task'].create({
                            'name': task_name,
                            'project_id': self.env['project.project'].search([], limit=1).id,
                        })

                        _logger.info("New task created: %s (ID: %s)", task.name, task.id)

                    # Get the analytic account from the task
                    account_id = task.analytic_account_id.id if task.analytic_account_id else None
                    if not account_id:
                        raise ValidationError(_('No analytic account set for task "%s" at line %d.') % (task.name, index))

                    # Create the timesheet entry
                    self.env['account.analytic.line'].create({
                        'date': date,
                        'name': name,
                        'unit_amount': float(hours),
                        'employee_id': user_employee.id,
                        'task_id': task.id,
                        'account_id': account_id,
                    })

                    _logger.info("Timesheet entry created for employee %s on task %s.", user_employee.name, task.name)

                except Exception as e:
                    _logger.error("Error on line %d: %s", index, str(e))
                    raise ValidationError(_('Error on line %d: %s') % (index, str(e)))


        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
