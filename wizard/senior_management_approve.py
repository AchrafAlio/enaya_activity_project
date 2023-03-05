from odoo import fields, models
from datetime import date

class CreateSeniorManagementApproveWizard(models.TransientModel):
    _name = "enayah.senior.management.approve.wizard"
    _description = "Senior Management Approve Wizard"

    remarks = fields.Char(string="Remarks", required=True)

    def confirm_remarks_am(self):
        active_id = self.env.context.get('active_id')
        rec = self.env['enayah.activity'].browse(active_id)
        rec.remarks = str(self.remarks)
        rec.action_modification_request()


    def need_senior_management_approval(self):
        active_id = self.env.context.get('active_id')
        rec = self.env['enayah.activity'].browse(active_id)
        rec.remarks = str(self.remarks)
        if rec.env.user.has_group('activity_execution_request.group_enayah_administration_manager'):
            rec.action_executive_director_approval()
        elif rec.env.user.has_group('activity_execution_request.group_enayah_executive_director'):
            rec.action_secretary_general_approval()


    def confirm_approve_by_am(self):
        active_id = self.env.context.get('active_id')
        rec = self.env['enayah.activity'].browse(active_id)
        if rec.remarks:
            rec.remarks = str(rec.remarks) + '\n' + str(self.remarks)
        else:
            rec.remarks = str(self.remarks)

        active_id = self.env.context.get('active_id')
        rec = self.env['enayah.activity'].browse(active_id)
        note_text = "Activity : " + rec.name + "\nStart date : " + rec.start_date_time.strftime(
            "%Y-%m-%d, %H:%M:%S")
        summary_text = "ACTIVITY " + rec.name + " APPROVED"
        # notify applicant
        rec.activity_schedule('activity_execution_request.mail_notify_applicant',
                           date_deadline=date.today(),
                           user_id=rec.create_uid.id,
                           note=note_text,
                           summary=summary_text,
                           activity_type_id=1)

        # notify concerned employees with start date of the activity
        for employee in rec.employee_ids:
            rec.activity_schedule('activity_execution_request.mail_notify_applicant',
                                  date_deadline=date.today(),
                                  user_id=employee.id,
                                  note=note_text,
                                  summary=summary_text,
                                  activity_type_id=1)
        rec.state = 'approved_by_administration_manager'
