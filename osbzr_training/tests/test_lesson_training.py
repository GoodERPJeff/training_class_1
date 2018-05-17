# -*- encoding: utf-8 -*-
from odoo.tests.common import   TransactionCase
class TestTraining(TransactionCase):
    def test_create(self):
        self.env['training.lesson'].create(
            {
               "start_date":"2018-05-20",
                "end_date":"2018-06-01",
                "name":"自动测试创建课程",
                "sites":"10"
            }
        )
