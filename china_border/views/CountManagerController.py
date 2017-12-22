#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表
@app.route('/countmanager/list', methods=['GET'])
@app.route('/countmanager/list/<currentpage>', methods=['GET'])
@app.route('/countmanager/list/<currentpage>/<sumpage>', methods=['GET'])
def countmanager_list(currentpage=1, sumpage=8):
    try:
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        #已经可以释放的账号
        sql="select id from bj_company_user where statu=2 and now()>end_time+ '1 day'"
        rows=getSelectSql(sql)
        length=len(rows)
        if length>0:
            uids='('
            if length==1:
                uids+=str(rows[0][0])
            else:
                for r in rows:
                    uids+=str(r[0])+','
            uids=uids[:-1]
            uids+=')'
            sql="update bj_company_user set statu=3,start_time=null,end_time=null where id in %s"%(uids)
            updateSql(sql)

        # for r in rows:
        #     sql="select 1 from bj_company_user where start_time<=now() and now()<=end_time and id='%s'"
        #     updateSql(sql)

        tsql="select bcu.id,bcu.name,bcu.password,bcu.start_time,bcu.end_time,bcu.statu,bc.name as cname from bj_company_user bcu left join bj_company bc on bc.id=bcu.companyid where 1=1"
        countsql="select count(1) from bj_company_user bcu left join bj_company bc on bcu.companyid=bc.id where 1=1"
        if key:
            tsql+=" and bcu.name like '%%%%%s%%%%' or bc.name like '%%%%%s%%%%'"%(key,key)
            countsql+=" and bcu.name like '%%%%%s%%%%' or bc.name like '%%%%%s%%%%'"%(key,key)
        tsql+="  order by bcu.create_date limit %s offset %s"%(sumpage,offset)
        trow=getSelectSql(tsql)

        countresult=getSelectSql(countsql)
        if(countresult[0][0]%sumpage==0):
            countpage=countresult[0][0]/sumpage
        else:
            countpage=countresult[0][0]/sumpage+1
        resp= render_template('CountManager/List.html', basepath=BASEPATH,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/countmanager/add', methods=['GET'])
def countmanager_add():
    try:
        psql="select id,name from bj_company"
        companies=getSelectSql(psql)
        resp= render_template('CountManager/Add.html', basepath=BASEPATH,companies=companies)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#账户禁用
@app.route('/countmanager/ban/<uids>', methods=['GET'])
def countmanager_ban(uids):
    try:
        resp= render_template('CountManager/Ban.html', basepath=BASEPATH,uids=uids)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/countmanager/edit/<id>', methods=['GET'])
def countmanager_edit(id):
    try:
        psql="select id,name from bj_company"
        companies=getSelectSql(psql)

        sql="select name,password,companyid,id from bj_company_user where id='%s'"%(id)
        uinfo=getSelectSql(sql)
        resp= render_template('CountManager/Edit.html', basepath=BASEPATH,companies=companies,uinfo=uinfo)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户保存
@app.route('/countmanager/save', methods=['POST'])
def countmanager_save():
    try:
       name = request.form.get('name')
       pwd = request.form.get('pwd')
       com = request.form.get('com')

       cid=request.form.get('id')
       mytime=time.strftime( ISOTIMEFORMAT, time.localtime() )
       if cid:
           tsql="update bj_company_user set name='%s',password='%s',companyid='%s' where id='%s'"%(name, pwd, com,cid)
       else:
           tsql = "insert into bj_company_user(name,password,companyid,create_date,statu) values('%s','%s','%s','%s','3')" % (name, pwd, com,mytime)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#用户账号禁用保存
@app.route('/countmanager/bansave', methods=['POST','GET'])
def countmanager_bansave():
    try:
       if request.method=='GET':
           uids=request.args.get('uids')
           uids=uids.split(',')
           for u in uids:
               tsql = "update bj_company_user set start_time=null,end_time=null,statu='3' where id='%s'" % (u)
               updateSql(tsql)
           return '0'

       uids = request.form.get('uids')
       start_time = request.form.get('start_time')
       end_time = request.form.get('end_time')
       uids=uids.split(',')
       for u in uids:
           tsql = "update bj_company_user set start_time='%s',end_time='%s',statu='%s' where id='%s'" % (start_time, end_time, 2, u)
           updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户具体页面
@app.route('/countmanager/detail/<id>', methods=['GET'])
def countmanager_detail(id):
    try:
        sql="select bcu.id,bcu.name,bcu.password,bc.name as cname,case when bcu.statu=3 then '启用' else '停用' end as statu,bcu.start_time,bcu.end_time from bj_company_user bcu left join bj_company bc on bc.id=bcu.companyid where bcu.id='%s'"%(id)
        uinfo=getSelectSql(sql)
        resp= render_template('CountManager/Detail.html', basepath=BASEPATH,uinfo=uinfo)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/countmanager/delete/<id>', methods=['GET'])
def countmanager_delete(id):
    try:
       tsql="delete from bj_company_user where id=%s"%(id)
       updateSql(tsql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp
