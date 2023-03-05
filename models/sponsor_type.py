# -*- coding: utf-8 -*-
from odoo import fields, models


class EnayahSponsorType(models.Model):
    _name = 'enayah.sponsor.type'
    _description = "Enayah Sponsor Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True, required=True)
    description = fields.Char(string='Description', tracking=True)

