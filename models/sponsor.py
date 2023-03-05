# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EnayahSponsor(models.Model):
    _inherit = 'res.partner'
    _description = "Enayah Sponsor"

    state = fields.Selection([('new', 'New'),
                              ('approved','Approved'),
                              ('old_discontinues', 'Old Discontinues'),
                              ('old_continuous', 'Old Continuous') ],
                            string='Status', default="new")
    sponsor_type_id = fields.Many2one("enayah.sponsor.type",string="Type")

    def action_approved(self):
        for rec in self:
            if rec.state == 'new':
                rec.state = 'approved'
            elif rec.state == 'old_discontinues':
                rec.state = 'old_continuous'

    def action_old_discontinues(self):
        for rec in self:
            if rec.state == 'approved' or rec.state == 'old_continuous':
                rec.state = 'old_discontinues'

