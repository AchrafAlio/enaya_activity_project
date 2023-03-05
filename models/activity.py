# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from datetime import date
from odoo.exceptions import ValidationError

class EnayahActivity(models.Model):
    _name = "enayah.activity"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Enayah Activity"

    name = fields.Char(string='Name', tracking=True, readonly="True", copy=False, default=lambda self: _('New'))
    user_id = fields.Many2one(comodel_name="res.users", string="User ID")
    state = fields.Selection([('new', 'New'),
                              ('administration_manager_approval', 'Administration Manager Approval'),
                              ('modification_request', 'Modification Request'),
                              ('approved_by_administration_manager', 'Approved By Administration Manager'),
                              ('executive_director_approval', 'Executive Director Approval'),
                              ('secretary_general_approval', 'Secretary General Approval'),
                              ('approved_by_secretary_general', 'Approved By Secretary General'),
                              ('reject', 'Rejected')], string='Status', default="new", tracking=True)
    type_activity_id = fields.Many2one(comodel_name='mail.activity.type',string="Type of Activity",tracking=True,
                                       required=True)
    submit_date = fields.Date(string="Submit Date")
    remarks = fields.Char(string="Activity Remarks", tracking=True)
    can_edit = fields.Boolean(string="Cant Edit", compute="_can_edit_compute", default=lambda self : True )
    start_date_time = fields.Datetime(string="Start Date", tracking=True, required=True)
    goal = fields.Text(string="Goal")
    employee_ids = fields.Many2many(comodel_name="res.users", string="Concerned Employees", tracking=True)
    hide_reject_button = fields.Boolean(compute="_hide_reject_button",default=False)
    hide_submit_button = fields.Boolean(default=True)
    hide_delete_button = fields.Integer(default=0)
    enaya_program_project_id = fields.Many2one(comodel_name="project.project", string="Program / Project",
                                               required=True,tracking=True)
    check_notify = fields.Boolean(default=False)
    sponsor_id = fields.Many2one(comodel_name="res.partner",domain=[('state', 'in', ['approved','old_continuous'])],
                                 string="Sponsor", required=True, tracking=True)
    sponsor_type = fields.Many2one('enayah.sponsor.type',string="Sponsor Type", related="sponsor_id.sponsor_type_id")
    sponsor_state = fields.Selection(string="Sponsor State", related="sponsor_id.state")


    am_id = fields.Many2one(comodel_name="res.users", string="Administration Manager ID", compute="_get_am_id")

    def _hide_reject_button(self):
        """
        function to hide reject button in certain cases
        :return: None
        """
        if self.env.user.has_group('activity_execution_request.group_enayah_applicant'):
            self.hide_reject_button = True
        elif self.env.user.has_group('activity_execution_request.group_enayah_administration_manager') and not(self.state == 'administration_manager_approval'):
            self.hide_reject_button = True
        elif self.env.user.has_group('activity_execution_request.group_enayah_executive_director') and (not self.state == 'executive_director_approval'):
            self.hide_reject_button = True
        elif self.env.user.has_group('activity_execution_request.group_enayah_secretary_general') and (not self.state == 'secretary_general_approval'):
            self.hide_reject_button = True
        else:
            self.hide_reject_button = False

    def action_open_wizard(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("activity_execution_request.view_senior_management_approve_form")
        action['res_id'] = self.id
        return action

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('enayah.activity') or _('New')
        vals['submit_date'] = datetime.datetime.now()
        vals['hide_submit_button'] = False
        return super(EnayahActivity, self).create(vals)


    def action_executive_director_approval(self):
        self.state = 'executive_director_approval'

    def action_modification_request(self):
        # notify applicant
        self.activity_schedule('activity_execution_request.mail_notify_applicant',
                               date_deadline=date.today(),
                               user_id=self.create_uid.id,
                               note=self.remarks,
                               summary = 'Modify your activity',
                               activity_type_id = 4
                            )
        self.state = 'modification_request'
        self.hide_submit_button = False


    def action_secretary_general_approval(self):
        self.state = 'secretary_general_approval'

    def action_approved_by_secretary_general(self):

        note_text = "Activity : " + self.name + "\nStart date : " + self.start_date_time.strftime(
                "%Y-%m-%d, %H:%M:%S")
        summary_text = "ACTIVITY " + self.name + " APPROVED"
        # notify applicant
        self.activity_schedule('activity_execution_request.mail_notify_applicant',
                               date_deadline=date.today(),
                               user_id=self.create_uid.id,
                               note=note_text,
                               summary=summary_text,
                               activity_type_id=1
                               )
        # notify concerned employees with start date of the activity
        for employee in self.employee_ids:
            self.activity_schedule('activity_execution_request.mail_notify_applicant',
                                  date_deadline=date.today(),
                                  user_id=employee.id,
                                  note=note_text,
                                  summary=summary_text,
                                  activity_type_id=1)
        self.remarks = "APPROVED BY SECRETARY GENERAL"
        self.state = 'approved_by_secretary_general'

    def action_reject(self):
        # notify applicant
        self.activity_schedule('activity_execution_request.mail_notify_applicant',
                               date_deadline=date.today(),
                               user_id=self.create_uid.id,
                               note="YOUR ACTIVITY IS CANCELED",
                               summary='ACTIVITY CANCEL',
                               activity_type_id=1
                               )
        self.state = 'reject'


    def action_submit(self):
        if self.state == 'new' or self.state=='modification_request':
            self.state = 'administration_manager_approval'
            note_text = "Please study this activity application request for approval"
            summary_text = "Activity Created"
            self.activity_schedule('activity_execution_request.mail_notify_am_create_activity',
                                   date_deadline=date.today(),
                                   user_id=self.am_id.id,
                                   note= note_text,
                                   summary= summary_text,
                                   activity_type_id=1
                                   )
        self.hide_submit_button = True


    def _can_edit_compute(self):
        self.can_edit = False
        if self.env.user.has_group('activity_execution_request.group_enayah_applicant') and self.state == 'new' and self.env.user.id== self.create_uid.id:
            self.can_edit = True
        elif self.env.user.has_group('activity_execution_request.group_enayah_applicant') and self.state == 'modification_request'and self.env.user.id== self.create_uid.id:
            self.can_edit = True
        else:
            self.can_edit = False


    def action_print_speach(self):
        return self.env.ref('activity_execution_request.report_sponsor_speach').report_action(self)


    def _get_am_id(self):
        """
        there is only one administration manager in the company
        :return: user with administration manager group
        """
        users_obj = self.env['res.users']
        for user in users_obj.search([]):
            if user.has_group("activity_execution_request.group_enayah_administration_manager"):
                self.am_id = user.id
                break

    def check_dates(self, current_date,start_date ):
        """
        start_date must be greater than current_date
        :param current_date:
        :param start_date:
        :return: None
        """
        current_date = current_date.strftime("%Y-%m-%d, %H:%M:%S")
        start_date = start_date.strftime("%Y-%m-%d, %H:%M:%S")
        if current_date > start_date:
            raise ValidationError(_("Start Date cannot be set before Current Date."))

    @api.onchange('start_date_time')
    def check_start_date_time(self):
        """
        Checks validity of start_date_time
        :return: None
        """
        if self.start_date_time:
            self.check_dates(datetime.datetime.now(), self.start_date_time)
