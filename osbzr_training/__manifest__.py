# -*- encoding: utf-8 -*-
{
    'name': 'osbzr_traning',
    'version': '1.0',
    'author': 'Mr Jeff',
    'category': 'osbzr',
    'price': '0.99',
    'summary': '跟jeff学二次开发实操项目',
    'license': 'GPL-2',
    'description':
        """
    用于开阖openerp培训实例
    """,
    'website': 'https://github.com/GoodERPJeff/training_class_1',
    'depends': ["mail"],
    'auto_install': False,
    'data': ["data/groups.xml", "osbzr_training_view.xml", "ir.model.access.csv", "report.xml"],
    'demo': ["data/training_demo.xml"],
#    'qweb': ["static/template.xml"],
}
