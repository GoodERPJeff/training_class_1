# -*- encoding: utf-8 -*-
import odoo
from odoo import http


class px(odoo.addons.web.controllers.main.Home):
    @http.route(['/px'], type='http', auth='user')
    def px2(self, *args, **kargs):
        teachers = []
        for p in http.request.env['res.partner'].search([('is_teacher','=',1)]):
            teachers.append(p.name)

        return http.request.render('osbzr_training.index', {'teachers':teachers})

