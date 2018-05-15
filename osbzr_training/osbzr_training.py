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

    @api.multi
    def name_get(self):
        '''
        科目名称从id翻译成名称时，追加显示科目管理人 如果在列表不显示管理人，form显示管理人
        :return:
        '''

        res=super(training_subject,self).name_get()

        result=[];
        print(self.env.context)
        if self.env.context.get('is_form'):
            for ele in res:
                result.append((ele[0],ele[1] + '-' + self.browse(ele[0]).manager_id.name))
        else:
            result=res
        return  result

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
    student_ids = fields.Many2many(comodel_name='res.partner', string="学生" )
    state=fields.Selection([('new','招生'),('start','已开课'),('end','已结束')],"课程状态",default='new')


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

    @api.multi
    def write(self, vals):
        if 'start_date' in vals.keys() or 'end_date' in vals.keys():
            for les in self:
                if les.state != 'new':
                    raise exceptions.ValidationError(u"已开课后日期不能修改！")
        return  super(training_lesson,self).write(vals)



    @api.multi
    def start(self):
        for lesson in self:
            self.state='start'

    @api.multi
    def unlink(self):
        print(self.env.context)
        return super(training_lesson,self).unlink()

    @api.multi
    def end(self):
        for lesson in self:
            self.state='end'


    _sql_constraints = [
        ('uniq_name','unique(name)','课程名字必须唯一')
    ]


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _is_teacher(self):
        return self.env.context.get('is_teacher')
    #提取xml字段里面定义的老师标记，决定是否默认为老师

    is_teacher=fields.Boolean(u'是老师',default=_is_teacher)


