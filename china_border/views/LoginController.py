#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,User,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar,hashlib,uuid

@app.route('/manager/login', methods=['GET'])
def login():
    resp= render_template('login.html', basepath=BASEPATH)
    return resp

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()
@app.route('/checklogin',methods=['post','get'])
def checklogin():
    username = request.form['username']
    password = request.form['password']
    try:
        if username is None or password is None:
            result = {
                "status": "error",
                "message": "用户名、密码不能为空！",
            }
        else:
            find_weixin_id = "select id from bj_company_user where name ='%s' and password='%s'" % (username,password)
            rows = getSelectSql(find_weixin_id)
            if len(rows)>0:
                uid = rows[0][0]

                sql="select main_count from bj_company_user where id='%s'"%(uid)
                row=getSelectSql(sql)
                if row[0][0]:
                    fid=row[0][0]
                else:
                    fid=uid
                # 已经可以释放的账号
                sql = "select id from bj_company_user where statu=2 and now()>end_time+ '1 day' and id='%s'"%(fid)
                rows = getSelectSql(sql)
                length = len(rows)
                if length > 0:
                    uids = '('
                    if length == 1:
                        uids += str(rows[0][0])
                    else:
                        for r in rows:
                            uids += str(r[0]) + ','
                    uids = uids[:-1]
                    uids += ')'
                    sql = "update bj_company_user set statu=3,start_time=null,end_time=null where id in %s" % (uids)
                    updateSql(sql)

                sql="select 1 from bj_company_user where id='%s' and statu=3"%(fid)
                row=getSelectSql(sql)
                if len(row)>0:
                    #从odoo校验身份成功之后
                    #由flask-login设置session和cookie
                    user = User()

                    vcode = uuid.uuid1()
                    user.vcode = vcode
                    user.id = uid
                    flask_login.login_user(user)
                    result = {
                        "status": "ok",
                        "message": "登录成功！",
                    }
                else:
                    result = {
                        "status": "error",
                        "message": "该账号暂停使用！",
                    }
            else:
                result = {
                    "status": "error",
                    "message": "用户名或密码错误！",
                }

    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        result = {
            "status": "error",
            "message": '错误:%s' % e,
        }
    return json.dumps(result, ensure_ascii=False)


@app.route('/manager/changepwd', methods=['GET'])
@flask_login.login_required
def manager_changepwd():
    resp= render_template('changepwd.html', basepath=BASEPATH)
    return resp

@app.route('/manager/changepwdpost', methods=['POST'])
@flask_login.login_required
def manager_changepwdpost():
    id=flask_login.current_user.id
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    new2password = request.form.get('new2password')
    msg=[]
    if newpassword!=new2password:
        msg.append({
            "state":"500",
            "msg":"新密码两次输入不同！"
            }
        )
    else:
        tsql="select * from bj_user where id=%s and password='%s'"%(id,oldpassword)
        trow=getSelectSql(tsql)
        if(len(trow)>0):
            isql="update bj_user set password='%s' where id=%s"%(newpassword,id)
            updateSql(isql)
            msg.append({
            "state":"200",
            "msg":"密码修改成功！"
            }
            )
        else:
            msg.append({
            "state":"500",
            "msg":"原密码错误！"
            }
            )
    return json.dumps(msg, ensure_ascii=False)