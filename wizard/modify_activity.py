from odoo import api, fields, models, _

class CreateModifyActivityWizard(models.TransientModel):
    _name = "enayah.modify.activity.wizard"
    _description = "Modify Activity Wizard"

    remarks = fields.Char(string="Remarks", required=True)

    def confirm_remarks(self):
        active_id = self.env.context.get('active_id')
        rec = self.env['enayah.activity'].browse(active_id)
        rec.remarks =  str(self.remarks)
        rec.action_modification_request()
