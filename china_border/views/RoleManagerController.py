#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表
@app.route('/rolemanager/list', methods=['GET'])
@app.route('/rolemanager/list/<currentpage>', methods=['GET'])
@app.route('/rolemanager/list/<currentpage>/<sumpage>', methods=['GET'])
def rolemanager_list(currentpage=1, sumpage=8):
    try:
        sys = flask_login.current_user.sys
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        tsql="select id,create_date,name,remark from bj_role where sys='%s'"%(sys)
        countsql="select count(1) from bj_role where sys='%s'"%(sys)
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
        resp= render_template('RoleManager/List.html', basepath=BASEPATH,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/rolemanager/add', methods=['GET'])
def rolemanager_add():
    try:
        sql="select id,name from bj_menu where pid='0' and sys='2'"
        rows=getSelectSql(sql)
        resp= render_template('RoleManager/Add.html', basepath=BASEPATH,rows=rows)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/rolemanager/edit/<id>', methods=['GET'])
def rolemanager_edit(id):
    try:
        sql="select id,name from bj_menu where pid='0' and sys='2'"
        allmenues=getSelectSql(sql)

        tsql="select name,remark,id from bj_role where id='%s'"%(id)
        role=getSelectSql(tsql)

        sql="select menu_ref from bj_role_menu where role_ref='%s'"%(id)
        menus=getSelectSql(sql)

        resp= render_template('RoleManager/Edit.html', basepath=BASEPATH,role=role,allmenues=allmenues,menus=menus)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#角色保存
@app.route('/rolemanager/save', methods=['POST'])
def rolemanager_save():
    try:
       name = request.form.get('name')
       menus = request.form.get('menus')
       remark = request.form.get('remark')
       mids=menus.split(',')
       role_id = request.form.get('id')
       if role_id:
           tsql = "update bj_role set name='%s',remark='%s' where id=%s" % (name, remark, role_id)
           updateSql(tsql)
           sql="delete from bj_role_menu where role_ref='%s'"%(role_id)
           updateSql(sql)
       else:
           sys = flask_login.current_user.sys
           createpams={
               "name":name,
               "remark":remark,
               "sys":sys
           }
           role_id = server.execute(info['db'], 1, info['password'], "bj.role", "create", createpams)

       for m in mids:
           sql="insert into bj_role_menu(role_ref,menu_ref) values('%s','%s')"%(role_id,m)
           updateSql(sql)
       return '1'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#部门具体页面
@app.route('/rolemanager/detail/<id>', methods=['GET'])
def rolemanager_detail(id):
    try:
        tsql="select create_date,name,remark from bj_role where id='%s'"%(id)
        role=getSelectSql(tsql)

        sql="select name from bj_menu where id in (select menu_ref from bj_role_menu where role_ref ='%s')"%(id)
        menus=getSelectSql(sql)

        resp= render_template('RoleManager/Detail_new.html', basepath=BASEPATH,role=role,menus=menus)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/rolemanager/delete/<id>', methods=['GET'])
def rolemanager_delete(id):
    try:
       sql="delete from bj_role_menu where role_ref='%s'"%(id)
       updateSql(sql)
       tsql="delete from bj_role where id=%s"%(id)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp
