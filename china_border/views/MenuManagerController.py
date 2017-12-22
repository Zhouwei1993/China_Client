#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表
@app.route('/menumanager/list', methods=['GET'])
@app.route('/menumanager/list/<currentpage>', methods=['GET'])
@app.route('/menumanager/list/<currentpage>/<sumpage>', methods=['GET'])
def menumanager_list(currentpage=1, sumpage=8):
    try:
        uid = flask_login.current_user.id
        sql="select 1 from bj_company_user where id='%s' and name='zw19930329'"%(uid)
        row=getSelectSql(sql)
        zw='0'
        if len(row)>0:
            zw='1'
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        tsql="select bm.id,bm.name,bm1.name as pname,bm.url,bm.remark from bj_menu bm left join bj_menu bm1 on bm.pid=bm1.id where bm.sys='2'"
        countsql="select count(1) from bj_menu where sys='2'"
        if key:
            tsql+=" and bm.name like '%%%%%s%%%%'"%(key)
            countsql+=" and name like '%%%%%s%%%%'"%(key)
        tsql+="  order by bm.create_date desc limit %s offset %s"%(sumpage,offset)
        trow=getSelectSql(tsql)
        countresult=getSelectSql(countsql)
        if(countresult[0][0]%sumpage==0):
            countpage=countresult[0][0]/sumpage
        else:
            countpage=countresult[0][0]/sumpage+1
        resp= render_template('MenuManager/List.html', basepath=BASEPATH,zw=zw,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/menumanager/add', methods=['GET'])
def menumanager_add():
    try:
        psql="select id,name from bj_menu where pid=0 and sys='2'"
        prow=getSelectSql(psql)
        resp= render_template('MenuManager/Add.html', basepath=BASEPATH,menus=prow)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/menumanager/edit/<id>', methods=['GET'])
def menumanager_edit(id):
    try:
        psql="select id,name,url,pid,remark from bj_menu where id='%s'"%(id)
        prow=getSelectSql(psql)
        rsql="select id,name from bj_menu where pid='0' and sys='2'"
        rrow=getSelectSql(rsql)
        resp= render_template('MenuManager/Edit.html', basepath=BASEPATH,menus=rrow,menu=prow)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户保存
@app.route('/menumanager/save', methods=['POST'])
def menumanager_save():
    try:
       name = request.form.get('name')
       url = request.form.get('url')
       pid = request.form.get('menu')
       remark = request.form.get('remark')
       id=request.form.get('id')
       mytime=time.strftime( ISOTIMEFORMAT, time.localtime() )
       if not pid:
           pid=0
       if id:
           tsql="update bj_menu set name='%s',url='%s',pid='%s',remark='%s' where id='%s'"%(name,url,pid,remark,id)
       else:
           tsql="insert into bj_menu(name,url,pid,remark,create_date,sys) values('%s','%s','%s','%s','%s','2')"%(name,url,pid,remark,mytime)
       rs=updateSql(tsql)
       if rs==1:
           return '1'
       else:
           return 0
       return redirect(url_for("menumanager_list"))
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#用户具体页面
@app.route('/menumanager/detail/<id>', methods=['GET'])
def menumanager_detail(id):
    try:
        psql = "select bm.id,bm.name,bm.url,bm.remark,bm1.name as pname from bj_menu bm left join bj_menu bm1 on bm1.id=bm.pid where bm.id='%s'" % (id)
        menu=getSelectSql(psql)
        resp= render_template('MenuManager/Detail.html', basepath=BASEPATH,menu=menu)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/menumanager/delete/<id>', methods=['GET'])
def menumanager_delete(id):
    try:
       sql="select 1 from bj_menu where pid='%s'"%(id)
       row=getSelectSql(sql)
       if len(row)>0:
           return '1'
       tsql="delete from bj_menu where id=%s"%(id)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp
