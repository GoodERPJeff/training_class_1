# -*- encoding: utf-8 -*-
#使用rpc访问odoo资源
from  xmlrpclib import ServerProxy
import datetime
HOST='127.0.0.1'
PORT=8069
DB='lesson'
USER='6658753@qq.com'
PASS = '6658753'
url='http://%s:%d/xmlrpc/' % (HOST,PORT)
obj_p=ServerProxy(url+'object')  #读取课程
for i in range(100):
    s_ret = obj_p.execute(DB, 1, PASS, 'training.lesson', 'read', i, ['name', 'start_date'])
    # print(i,s_ret)


def get_remain_seats(pRetId):
    lesson = (obj_p.execute(DB, 1, PASS, 'training.lesson', 'read', pRetId,
                            ['name', 'sites', 'start_date', 'remain_seats']));  # 读取课程资料
    print(lesson[0].get('sites'))
    sites = lesson[0].get('remain_seats')
    print('%s的总席位数为%d剩余席位数为%d' % (lesson[0].get('name'),
                                  lesson[0].get('sites'),
                                  lesson[0].get('remain_seats')
                                  )
          )

#创建一个课程
iRetId=obj_p.execute(DB, 1, PASS, 'training.lesson', 'create',{"name":'rpc op test16' + str(datetime.datetime.now()),
                                                               "subject_id":"5", "start_date":"2018-09-15",
                                                               "end_date":"2018-09-25","sites":"25",})
get_remain_seats(iRetId)

#报名 用课程表write执行报表
obj_p.execute(DB, 1, PASS, 'training.lesson', 'write', iRetId, {"student_ids":[(4,3),(4,8)]})

get_remain_seats(iRetId)

#取消3，8报名学生
obj_p.execute(DB, 1, PASS, 'training.lesson', 'write', iRetId, {"student_ids":[(3,3),(3,8)]})
get_remain_seats(iRetId)

#用向导对象报名
i_apply_id = obj_p.execute(DB, 1, PASS, 'training.apply', 'create',  {"lesson_id":iRetId,"student_ids":[(4,3),(4,8)]})

obj_p.execute(DB, 1, PASS, 'training.apply', 'do_apply', i_apply_id)
get_remain_seats(iRetId)