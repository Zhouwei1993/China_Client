#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#公司列表
@app.route('/cmanager/list', methods=['GET'])
@app.route('/cmanager/list/<currentpage>', methods=['GET'])
@app.route('/cmanager/list/<currentpage>/<sumpage>', methods=['GET'])
def cmanager_list(currentpage=1, sumpage=8):
    try:
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        tsql="select name,remark,id from bj_company where 1=1"
        countsql="select count(1) from bj_company where 1=1"
        if key:
            tsql+=" and name like '%%%%%s%%%%'"%(key)
            countsql+=" and name like '%%%%%s%%%%'"%(key)
        tsql+="  order by create_date limit %s offset %s"%(sumpage,offset)
        trow=getSelectSql(tsql)
        countresult=getSelectSql(countsql)
        if(countresult[0][0]%sumpage==0):
            countpage=countresult[0][0]/sumpage
        else:
            countpage=countresult[0][0]/sumpage+1
        resp= render_template('ComManager/List.html', basepath=BASEPATH,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/cmanager/add', methods=['GET'])
def cmanager_add():
    try:
        resp= render_template('ComManager/Add.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/cmanager/edit/<id>', methods=['GET'])
def cmanager_edit(id):
    try:
        tsql="select name,remark,id from bj_company where id='%s'"%(id)
        com=getSelectSql(tsql)
        resp= render_template('ComManager/Edit.html', basepath=BASEPATH,com=com)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#部门保存
@app.route('/cmanager/save', methods=['POST'])
def cmanager_save():
    try:
       name = request.form.get('name')
       remark = request.form.get('remark')
       mytime = time.strftime(ISOTIMEFORMAT, time.localtime())
       com_id = request.form.get('id')
       if com_id:
           tsql = "update bj_company set name='%s',remark='%s' where id=%s" % (name, remark, com_id)
       else:
           tsql = "insert into bj_company(name,remark,create_date) values('%s','%s','%s')" % (name, remark, mytime)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#部门具体页面
@app.route('/cmanager/detail/<id>', methods=['GET'])
def cmanager_detail(id):
    try:
        tsql="select create_date,name,remark from bj_company where id='%s'"%(id)
        com=getSelectSql(tsql)
        resp= render_template('ComManager/Detail.html', basepath=BASEPATH,com=com)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/cmanager/delete/<id>', methods=['GET'])
def cmanager_delete(id):
    try:
       tsql="delete from bj_company where id=%s"%(id)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp
