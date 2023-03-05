# -*- coding: utf-8 -*-
from odoo import fields, models

class EnayahProgramProject(models.Model):
    _inherit = "project.project"
    _description = "enayah program/project"

    speach_model = fields.Html(string="Speach Model", required=True)




