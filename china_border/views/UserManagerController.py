#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表
@app.route('/usermanager/list', methods=['GET'])
@app.route('/usermanager/list/<currentpage>', methods=['GET'])
@app.route('/usermanager/list/<currentpage>/<sumpage>', methods=['GET'])
def usermanager_list(currentpage=1, sumpage=8):
    try:
        roles = flask_login.current_user.roles
        if '超级管理员' in roles:
            is_administrator='1'
        else:
            is_administrator='0'
        key = request.args.get('key')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)

        tsql="select * from bj_company_user where 1=1"
        countsql="select count(1) from bj_company_user where 1=1"
        user_id = flask_login.current_user.id
        if is_administrator == '1':
            sql="select id from bj_company_user where companyid=(select companyid from bj_company_user where id='%s')"%(user_id)
            rows=getSelectSql(sql)
            if len(rows)>0:
                uids="("
                for r in rows:
                    uids+=str(r.id)+','
                uids=uids[:-1]+")"
            else:
                uids="(-1)"

            tsql+=" and id in %s"%(uids)
            countsql += " and id in %s" % (uids)

        else:
            tsql+=" and id='%s'"%(user_id)
            countsql += " and id='%s'" % (user_id)
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
        resp= render_template('UserManager/List.html',
                              basepath=BASEPATH,
                              userlist=trow,
                              offset=offset,
                              countpage=countpage,
                              currentpage=currentpage,
                              key=key,
                              is_administrator=is_administrator)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户增加
@app.route('/usermanager/add', methods=['GET'])
def usermanager_add():
    try:
        sys = flask_login.current_user.sys
        rsql="select id,name from bj_role where sys='%s'"%(sys)
        roles=getSelectSql(rsql)
        resp= render_template('UserManager/Add.html', basepath=BASEPATH,roles=roles)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户编辑
@app.route('/usermanager/edit/<id>', methods=['GET'])
def usermanager_edit(id):
    try:
        sys = flask_login.current_user.sys
        roles = flask_login.current_user.roles
        if '超级管理员' in roles:
            is_administrator='1'
        else:
            is_administrator='0'

        sql="select bu.id,bu.name,bu.password from bj_company_user bu where bu.id='%s'"%(id)
        user=getSelectSql(sql)
        sql="select bcur.role_ref,br.name from bj_companyuser_role bcur left join bj_role br on br.id=bcur.role_ref where bcur.user_ref='%s'"%(id)
        role=getSelectSql(sql)

        sql="select id,name from bj_role where sys='%s'"%(sys)
        roles=getSelectSql(sql)


        resp= render_template('UserManager/Edit.html',
                              basepath=BASEPATH,
                              user=user,
                              roles=roles,
                              role=role,
                              is_administrator=is_administrator)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户保存
@app.route('/usermanager/save', methods=['POST'])
def usermanager_save():
    try:
       user_id = flask_login.current_user.id
       companyid = flask_login.current_user.companyid
       name = request.form.get('name')
       pwd = request.form.get('pwd')
       role_ref = request.form.get('roles')
       uid=request.form.get('id')
       mytime=time.strftime( ISOTIMEFORMAT, time.localtime() )
       rids=role_ref.split(',')

       if uid:
           sql="delete from bj_companyuser_role where user_ref='%s'"%(uid)
           updateSql(sql)
           createpams = {
               "name": name,
               "password": pwd,
           }
           server.execute(info['db'], 1, info['password'], "bj.company.user", "write",int(uid), createpams)
       else:
           createpams = {
               "name": name,
               "password": pwd,
               "companyid":companyid,
               "main_count": user_id
           }
           uid = server.execute(info['db'], 1, info['password'], "bj.company.user", "create", createpams)
       for r in rids:
           if r:
               sql="insert into bj_companyuser_role(user_ref,role_ref) values('%s','%s')"%(uid,r)
               updateSql(sql)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


#用户具体页面
@app.route('/usermanager/detail/<id>', methods=['GET'])
def usermanager_detail(id):
    try:
        sql="select bu.id,bu.name,bu.password from bj_company_user bu  where bu.id='%s'"%(id)
        user=getSelectSql(sql)
        sql="select br.name from bj_companyuser_role bur left join bj_role br on bur.role_ref=br.id where bur.user_ref='%s'"%(id)
        roles=getSelectSql(sql)

        # sql="select id,name from bj_role"
        # roles=getSelectSql(sql)

        resp= render_template('UserManager/Detail.html', basepath=BASEPATH,user=user,roles=roles)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

#用户删除
@app.route('/usermanager/delete/<id>', methods=['GET'])
def usermanager_delete(id):
    try:
       sql="delete from bj_companyuser_role where user_ref='%s'"%(id)
       rs=updateSql(sql)
       print(rs)
       tsql="delete from bj_company_user where id=%s"%(id)
       rs=updateSql(tsql)
       print(rs)
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

