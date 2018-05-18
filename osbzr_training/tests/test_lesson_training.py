# -*- encoding: utf-8 -*-
from odoo.tests.common import   TransactionCase
from odoo.exceptions import  ValidationError
class TestTraining(TransactionCase):
    def test_create(self):
        #接受到错误，表示实现时做了检查
        with self.assertRaises(ValidationError):
            self.env['training.lesson'].create(
                {
                   "start_date":"2018-08-20",
                    "end_date":"2018-06-01",
                    "name":"自动测试创建课程",
                }
            )

