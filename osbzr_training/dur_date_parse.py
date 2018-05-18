# # -*- encoding: utf-8 -*-
# from odoo.report import report_sxw
# from datetime import datetime
# from odoo.osv import osv
#
#
# class LessonReportParse(report_sxw.rml_parse):
#     def __init__(self, cr, uid, name, context=None):
#         # -*- __init__调用的时候回调用
#         # init 安装模块的时候调用-*-
#         super(LessonReportParse, self).__init__(
#             cr, uid, name, context=context)
#         self.localcontext.update({
#             'durDates': self.durdates,
#         })
#
#     def durdates(self, start_date):
#         if start_date:
#             sdate = datetime.strptime(start_date, '%Y-%m-%d')
#             return (datetime.now - sdate).days
#         else:
#             return 0
#
#
# class ReportParse(osv.AbstractModel):
#     _name = 'report.osbzr_training.action_report_print_overdue'
#     _inherit = 'report.abstract_report'
#     _template = 'osbzr_training.report_lesson'
#     _wrapped_report_class = LessonReportParse
#     _description = u'开课时间计算'
