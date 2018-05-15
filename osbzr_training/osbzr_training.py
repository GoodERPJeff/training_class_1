# -*- encoding: utf-8 -*-
from odoo import models, fields, api,exceptions


class training_subject(models.Model):
    _name = 'training.subject'
    _rec_name = 'name'

    name = fields.Char(u'名称',
                        size=64,
                        required=True)

    manager_id = fields.Many2one(string= u'负责人',
                        comodel_name='res.users')

    lesson_ids = fields.One2many(comodel_name='training.lesson',inverse_name='subject_id',string='课程')

    description = fields.Text('描述')

class training_lesson(models.Model):
    _name = 'training.lesson'
    _rec_name = 'name'

    name = fields.Char(u'名称',
                        size=64,
                        required=True)

    subject_id = fields.Many2one(string= u'科目名称',
                        comodel_name='training.subject')

    start_date = fields.Date("开始日期")
    end_date = fields.Date("结束日期")
    sites = fields.Integer("座位数")
    teacher_id = fields.Many2one(comodel_name='res.partner',string="老师",domain="[('is_teacher','=',True)]")
    student_ids = fields.Many2many(comodel_name='res.partner', string="学生")

    @api.constrains('end_date', 'start_date')
    def check_edate(self):
        for lesson in self:
            if lesson.end_date < lesson.start_date:
                raise exceptions.ValidationError(u"开始日其不能晚于结束日期！")

    @api.constrains('sites')
    def check_edate(self):
        for lesson in self:
            if lesson.sites <= 0:
                raise exceptions.ValidationError(u"人数不能为0！")



class res_partner(models.Model):
    _inherit = 'res.partner'

    is_teacher=fields.Boolean(u'是老师')