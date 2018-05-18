# -*- encoding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import datetime


class TrainingSubject(models.Model):
    _name = 'training.subject'
    _rec_name = 'name'

    name = fields.Char(u'名称',
                       size=64,
                       required=True)

    manager_id = fields.Many2one(string=u'负责人',
                                 comodel_name='res.users')

    lesson_ids = fields.One2many(comodel_name='training.lesson', inverse_name='subject_id', string='课程')

    description = fields.Text('描述')

    @api.multi
    def name_get(self):
        """
        科目名称从id翻译成名称时，在科目名称后面增加显示科目管理人 （如果在tree里面不显示追加的管理人，在form中显示管理人）
        :return:
        """

        res = super(TrainingSubject, self).name_get()

        result = [];
        if self.env.context.get('is_form'):
            # 在xml文件的 training_lesson_form的subject_id中，用  context="{'is_form':'1'}" 写入标记
            # 在此处通过读取标记判断是从form进入
            for ele in res:
                result.append((ele[0], ele[1] + '-' + self.browse(ele[0]).manager_id.name))
        else:
            result = res
        return result


class TrainingLesson(models.Model):
    _name = 'training.lesson'
    _rec_name = 'name'
    _inherit = ["mail.thread"]

    name = fields.Char(u'名称',
                       size=64,
                       required=True)

    subject_id = fields.Many2one(string=u'科目名称',
                                 comodel_name='training.subject')
    start_date = fields.Date("开始日期" ,
                             track_visibility='onchange')
    end_date = fields.Date("结束日期")
    sites = fields.Integer("座位数")
    teacher_id = fields.Many2one(comodel_name='res.partner', string="老师", domain="[('is_teacher','=',True)]",
                                 ondelete='restrict')
    student_ids = fields.Many2many(comodel_name='res.partner', string="学生")
    state = fields.Selection([('new', '招生'), ('start', '已开课'),
                              ('end', '已结束')], string="课程状态", default='new',
                             track_visibility='aways')
    continue_days = fields.Integer(string='持续天数', compute='_get_continue_days', store=True)
    progress = fields.Float(string='报名进度', compute='_get_progress_and_remain_seats')
    remain_seats = fields.Float(string='剩下名额', compute='_get_progress_and_remain_seats', inverse='_inverse_seats',
                                store=True, digits=(16, 0))
    # inverse 反过来计算功能，如果没有该选项，计算字段不可编辑，如果指定的话，可以编辑用于反算
    manager_id = fields.Many2one('res.users', related='subject_id.manager_id', string='负责人', readonly=True, store=True)

    @api.depends('sites')
    def _inverse_seats(self):
        for lesson in self:
            lesson.sites = len(lesson.student_ids) + lesson.remain_seats

    @api.depends('sites', 'student_ids')
    def _get_progress_and_remain_seats(self):
        for lesson in self:
            if lesson.sites > 0:
                lesson.remain_seats = lesson.sites - len(lesson.student_ids)
                lesson.progress = round(float(len(lesson.student_ids)) / float(lesson.sites), 2) * 100
            # print(lesson.student_ids,lesson.sites,len(lesson.student_ids),round(len(lesson.student_ids) / lesson.sites,2))

    @api.depends('start_date', 'end_date')
    def _get_continue_days(self):
        for lesson in self:
            if lesson.start_date and lesson.end_date:
                start_date = datetime.strptime(lesson.start_date, '%Y-%m-%d')
                end_date = datetime.strptime(lesson.end_date, '%Y-%m-%d')
                lesson.continue_days = (end_date - start_date).days

    @api.constrains('end_date', 'start_date')
    def _check_edate(self):
        for lesson in self:
            if lesson.end_date < lesson.start_date:
                raise exceptions.ValidationError(u"开始日期不能晚于结束日期！")

    @api.constrains('sites')
    def _check_start_date_end_date(self):
        for lesson in self:
            if lesson.sites <= 0:
                raise exceptions.ValidationError(u"人数不能为0！")

    @api.multi
    def write(self, vals):
        if 'start_date' in vals.keys() or 'end_date' in vals.keys():
            for les in self:
                if les.state != 'new':
                    raise exceptions.ValidationError(u"已开课后日期不能修改！")
        return super(TrainingLesson, self).write(vals)

    @api.multi
    def start(self):
        for lesson in self:
            self.state = 'start'  # 写入state值到数据库

    @api.multi
    def unlink(self):  # 删除操作 context中会带有删除ids
        print(self.env.context)
        return super(TrainingLesson, self).unlink()

    @api.multi
    def end(self):
        for lesson in self:
            self.state = 'end'

    # 数据库约束，将在数据库创建约束
    _sql_constraints = [
        ('uniq_name', 'unique(name)', '课程名字必须唯一')
    ]


# 报名向导界面
class Apply(models.TransientModel):
    _name = 'training.apply'
    lesson_id = fields.Many2one(string="课程", comodel_name='training.lesson',
                                default = lambda self:self.env.context.get('active_id'))
    student_ids = fields.Many2many(string="报名学生", comodel_name='res.partner')
    state = fields.Selection([('new', '招生'), ('start', '已开课'), ('end', '已结束')], string="课程状态")

    @api.multi
    def do_apply(self):
        if self.lesson_id.state != 'new':
            raise exceptions.ValidationError(u"抱歉，报名已经结束，他们来晚了。")

        if self.lesson_id.sites <= len(self.student_ids) + len(self.lesson_id.student_ids):
            raise exceptions.ValidationError(u"抱歉，报名名额已满。")

        start_date = datetime.strptime(self.lesson_id.start_date, '%Y-%m-%d')
        if datetime.now() > start_date:
            raise exceptions.ValidationError(u"抱歉，课程已经开课，不能继续报名。")

        sIds = []
        for s in self.student_ids:
            if s in self.lesson_id.student_ids:
                raise exceptions.ValidationError(u"已经报名的学生，不能重复报名.")
            sIds.append((4, s.id))  # [(4,1),(4,2),(4.n)]
        self.lesson_id.write({'student_ids': sIds})  # 4新增已有id

        return{
            'name':u'报名的学生',
            'view_type':'form',
            'view_mode':'tree',
            'res_model':'res.partner',
            'type':'ir.actions.act_window',
            'domain':[('id','in',[s.id for s in self.student_ids])],
            'view_id':False,
        }
    # viewmode为tree传domain 为form传res


    @api.multi
    def do_pre_filter(self):
        return{
            'name':u'开课的学生tree',
            'view_type':'form',
            'view_mode':'tree',
            'res_model':'training.lesson',
            'type':'ir.actions.act_window',
            'domain':[('state','=','new')],
            'view_id':False,
        }



    @api.multi
    @api.onchange('lesson_id')
    def sync_state_on_chage(self):
        self.state = self.lesson_id.state


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _is_teacher(self):
        return self.env.context.get('is_teacher')

    # 提取xml字段里面定义的老师标记，决定是否默认为老师 default=一个函数
    is_teacher = fields.Boolean(u'是老师', default=_is_teacher)



