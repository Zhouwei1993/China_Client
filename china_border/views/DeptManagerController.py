#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表
@app.route('/deptmanager/list', methods=['GET'])
@app.route('/deptmanager/list/<currentpage>', methods=['GET'])
@app.route('/deptmanager/list/<currentpage>/<sumpage>', methods=['GET'])
def deptmanager_list(currentpage=1, sumpage=8):
    try:
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        tsql="select name,remark,id from bj_department where 1=1"
        countsql="select count(1) from bj_department where 1=1"
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
        resp= render_template('DeptManager/List.html', basepath=BASEPATH,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/deptmanager/add', methods=['GET'])
def deptmanager_add():
    try:
        resp= render_template('DeptManager/Add.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/deptmanager/edit/<id>', methods=['GET'])
def deptmanager_edit(id):
    try:
        tsql="select name,remark,id from bj_department where id='%s'"%(id)
        dept=getSelectSql(tsql)
        resp= render_template('DeptManager/Edit.html', basepath=BASEPATH,dept=dept)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#部门保存
@app.route('/deptmanager/save', methods=['POST'])
def deptmanager_save():
    try:
       name = request.form.get('name')
       remark = request.form.get('remark')
       mytime = time.strftime(ISOTIMEFORMAT, time.localtime())
       dept_id = request.form.get('id')
       if dept_id:
           tsql = "update bj_department set name='%s',remark='%s' where id=%s" % (name, remark, dept_id)
       else:
           tsql = "insert into bj_department(name,remark,create_date) values('%s','%s','%s')" % (name, remark, mytime)
       updateSql(tsql)
       return '1'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#部门具体页面
@app.route('/deptmanager/detail/<id>', methods=['GET'])
def deptmanager_detail(id):
    try:
        tsql="select name,remark,id from bj_department where id='%s'"%(id)
        dept=getSelectSql(tsql)
        resp= render_template('DeptManager/Detail.html', basepath=BASEPATH,dept=dept)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/deptmanager/delete/<id>', methods=['GET'])
def deptmanager_delete(id):
    try:
       tsql="delete from bj_department where id=%s"%(id)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#企业号同步
@app.route('/deptmanager/synchronization/<id>', methods=['GET'])
def deptmanager_synchronization(id):
    try:
        tsql="select * from zdk_user where id=%s"%(id)
        trow=getSelectSql(tsql)[0]
        re=wcmgr.getWc_Sdk(6).addUser(trow.phone, trow.name, trow.phone,[1],None)
        if(re==0):
            msg={
                 "msg":"OK"
                }
        elif(re==60104):
            msg={
                "msg":"Exist"
            }
        else:
            msg={
                 "msg":"Error"
                }
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        msg.append={
                 "msg":"Error"
                }
    return json.dumps(msg,ensure_ascii=False)
