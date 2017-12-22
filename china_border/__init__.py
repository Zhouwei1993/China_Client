#coding=utf-8

from flask import Flask,make_response,redirect,json,render_template,url_for
from sqlalchemy import create_engine
import xmlrpc.client,flask_login,time,uuid
from wechatsdk import WC_SDK_BASE
from flask_apscheduler import APScheduler
app = Flask(__name__)
app.secret_key = '123456'
ISOTIMEFORMAT='%Y-%m-%d %X'
# BASEPATH= "http://bj.growhappy.cn/"
BASEPATH= "http://127.0.0.1:8877/"
# BASEPATH= "http://114.55.88.84:8877/"
# BASEPATH= "https://114.55.88.84:8877/"
server = xmlrpc.client.ServerProxy("http://114.55.88.84:8069/xmlrpc/object")
info = {'db': 'bj', 'password': 'admin'}
DBengine = create_engine('postgresql+psycopg2://odoo:admin@114.55.88.84:5432/bj')

def getCountSql(sql):
    """
    返回count语句的数量结果
    print("result:%s"%getCountSql("SELECT count(*) FROM zqt_doc"))
    :param sql:
    :return:
    """
    r = DBengine.execute(sql)
    ru = r.fetchall()[0][0]
    return ru


def updateSql(sql):
    """
    执行更新语句
    :param sql:
    :return:
    """
    r = DBengine.execute(sql)
    return r.rowcount

def getSelectSql(sql):
    """
    返回select语句的结果集
    :param sql:
    :return:
    """
    r = DBengine.execute(sql)
    return r.fetchall()

# from china_border.services.WeChatSdkManager import *
# wcmgr = WeChatSdkManager()
#
# # 定时任务
# from china_border.services.scheduler import *
# class Config(object):
#     JOBS = [
#             {
#                'id':'job1',
#                'func':downloadimg,
#                'args': '',
#                'trigger': {
#                     'type': 'cron',
#                     'hour':'4',
#                     'minute':'28',
#                     'second': '30'
#                 }
#              }
#         ]
# print("定时任务开启!")
# scheduler = APScheduler()
# app.config.from_object(Config())
# scheduler.init_app(app)
# scheduler.start()


# from xqd_edu_b.WeixinBaseCache import WeiXinBaseCache
# weiXinBaseCache = WeiXinBaseCache()
#***************************************************FLASK-LOGIN*********************************************************
#初始化loginmanager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self):
        self.cachedata = False
        self.name = False
        self.phoneno = False
        self.school_ids = False
        self.area_ids = False
        self.grade_ids = False
        self.class_ids = False
        self.teacher_id = False
        self.avatar=False
        self.roles = False
        self.companyid = False
        self.sys = False
        self.vcode = False
@login_manager.user_loader
def user_loader(uid):
    print("user_loader->uid:%s"%uid)
    """
    flask-login从session中将uid给用户
    查出用户的详细数据返回给业务
    :return:
    """
    #TODO从缓存中获取数据
    user = User()
    user.id = uid
    tsql="select name from bj_company_user where id=%s"%(uid)
    trow=getSelectSql(tsql)[0]
    user.name=trow[0]
    user.avatar=''
    user.phoneno=''
    sql="select br.name from bj_company_user bcu left join bj_companyuser_role bcur on bcur.user_ref=bcu.id left join bj_role br on br.id=bcur.role_ref where bcu.id='%s'"%(uid)
    rows=getSelectSql(sql)
    roles=[]
    if len(rows)>0:
        for r in rows:
            roles.append(r[0])
    user.roles=roles
    sql="select companyid from bj_company_user where id='%s'"%(uid)
    row=getSelectSql(sql)
    if len(row)>0:
        comid=row[0][0]
    else:
        comid=''
    user.companyid=comid

    sql="select br.sys from bj_company_user bcu left join bj_companyuser_role bcur on bcur.user_ref=bcu.id left join bj_role br on br.id=bcur.role_ref where bcu.id='%s' limit 1"%(uid)
    row=getSelectSql(sql)
    if len(row)>0:
        user.sys=row[0][0]
    vcode=uuid.uuid1()
    user.vcode=vcode
    return user

@login_manager.request_loader
def request_loader(request):
    """
    :param request:
    :return:
    """
    return

@login_manager.unauthorized_handler
def unauthorized_handler():
    #无权限则前往登陆画面
    return redirect(url_for("login"))

#***********************************************************************************************************************

import china_border.views.IndexController
import china_border.views.LoginController
import china_border.views.ManagerController
import china_border.views.UserManagerController
import china_border.views.DeptManagerController
import china_border.views.PatrolManagerController
import china_border.views.RoleManagerController
import china_border.views.CertController
import china_border.views.MenuManagerController
import china_border.views.ApplyManagerController
import china_border.views.CompanyManagerController
import china_border.views.CountManagerController
import china_border.views.ShangYouDataController
import china_border.views.ShangYouCrewsDataController
print('开始启动嘉兴边检服务')
