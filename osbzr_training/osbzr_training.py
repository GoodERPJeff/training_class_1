# -*- encoding: utf-8 -*-
from  odoo  import  models,fields
class training_subject(models.Model):
    _name = 'training.subject'
    _rec_name = 'name'

    name = fields.Char(u'名称',
                        size=64)
