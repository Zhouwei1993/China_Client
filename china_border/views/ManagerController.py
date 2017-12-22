#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
#5A后台管理
#5A后台管理主页
@app.route('/manager/index', methods=['GET'])
@flask_login.login_required
def manager_index():
    print(11)
    name=flask_login.current_user.name
    print(22)
    avatar=flask_login.current_user.avatar
    print(33)
    resp= render_template('Manager/Index.html', basepath=BASEPATH,name=name,avatar=avatar)
    return resp