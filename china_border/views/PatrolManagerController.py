#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表
@app.route('/patrolmanager/list', methods=['GET'])
@app.route('/patrolmanager/list/<currentpage>', methods=['GET'])
@app.route('/patrolmanager/list/<currentpage>/<sumpage>', methods=['GET'])
def patrolmanager_list(currentpage=1, sumpage=8):
    try:
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        tsql="select zp.id,case when zp.type=1 then '日常值班' when zp.type=2 then '领导值班' when zp.type=3 then '节假日值班' when zp.type=4 then '夜游值班' else '' end as zbtype,zp.content,case when zp.state=1 then '未处理' when zp.state=2 then '已处理' else '' end as state,zp.cl_result,zu.name from zdk_patrol zp left join zdk_user zu on zu.id=zp.sb_user where 1=1"
        countsql="select count(1) from zdk_patrol zp left join zdk_user zu on zu.id=zp.sb_user where 1=1"
        if key:
            tsql+=" and zu.name like '%%%%%s%%%%'"%(key)
            countsql+=" and zu.name like '%%%%%s%%%%'"%(key)
        tsql+="  order by zp.create_date limit %s offset %s"%(sumpage,offset)
        trow=getSelectSql(tsql)
        countresult=getSelectSql(countsql)
        if(countresult[0][0]%sumpage==0):
            countpage=countresult[0][0]/sumpage
        else:
            countpage=countresult[0][0]/sumpage+1
        resp= render_template('PatrolManager/List.html', basepath=BASEPATH,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/patrolmanager/add', methods=['GET'])
def patrolmanager_add():
    try:
        resp= render_template('PatrolManager/Add.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/patrolmanager/edit/<id>', methods=['GET'])
def patrolmanager_edit(id):
    try:
        patrol_type=[[1,"日常值班"],[2,"领导值班"],[3,"节假日值班"],[4,"夜游值班"]]
        tsql="select zp.id,zp.type,zp.content,zp.state,zp.cl_result,zu.name sbname,zu1.name as clname,zp.remark from zdk_patrol zp left join zdk_user zu on zu.id=zp.sb_user  left join zdk_user zu1 on zu1.id=zp.cl_user where zp.id='%s'"%(id)
        trow=getSelectSql(tsql)[0]
        resp= render_template('PatrolManager/Edit.html', basepath=BASEPATH,user=trow,patrol_type=patrol_type)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#部门保存
@app.route('/patrolmanager/save', methods=['POST'])
def patrolmanager_save():
    try:
       type = request.form.get('type')
       content = request.form.get('content')
       status = request.form.get('status')
       result = request.form.get('result')
       remark = request.form.get('remark')
       mytime = time.strftime(ISOTIMEFORMAT, time.localtime())
       patrol_id = request.form.get('id')
       if patrol_id:
           tsql = "update zdk_patrol set type='%s',content='%s',state='%s',cl_result='%s',remark='%s',create_date='%s' where id=%s" % (type,content,status,result, remark,mytime,patrol_id)
       else:
           pass
       updateSql(tsql)
       return redirect(url_for("patrolmanager_list"))
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#部门具体页面
@app.route('/patrolmanager/detail/<id>', methods=['GET'])
def patrolmanager_detail(id):
    try:
        tsql="select case when zp.type=1 then '日常值班' when zp.type=2 then '领导值班' when zp.type=3 then '节假日值班' when zp.type=4 then '夜游值班' else '' end as zbtype,zp.content,case when zp.state=1 then '未处理' when zp.state=2 then '已处理' else '' end as state,zp.cl_result,zu.name sbname,zu1.name as clname,zp.remark from zdk_patrol zp left join zdk_user zu on zu.id=zp.sb_user  left join zdk_user zu1 on zu1.id=zp.cl_user where zp.id='%s'"%(id)
        trow=getSelectSql(tsql)[0]
        resp= render_template('PatrolManager/Detail.html', basepath=BASEPATH,user=trow)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/patrolmanager/delete/<id>', methods=['GET'])
def patrolmanager_delete(id):
    try:
       tsql="delete from zdk_patrol where id=%s"%(id)
       updateSql(tsql)
       return redirect(url_for("patrolmanager_list"))
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp



