#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
ISOTIMEFORMAT='%Y-%m-%d %X'

@app.route('/cert/menu', methods=['GET'])
def cert_menu():
    try:
        user_id = flask_login.current_user.id

        #根据用户搜索出对应的角色
        sql="select role_ref from bj_companyuser_role where user_ref='%s'"%(user_id)
        rows=getSelectSql(sql)

        rids='('
        length=len(rows)
        if length>1:
            for r in rows:
                rids+=str(r[0])+','
            rids=rids[:-1]
            rids+=')'
        elif length==1:
            rids+=str(rows[0][0])+')'
        else:
            rids='(-1)'

        #根据角色搜索到对应的菜单
        sql="select bm.id,bm.name,bm.is_last,bm.pid,bm.url from bj_menu bm " \
            "left join bj_role_menu brm on brm.menu_ref=bm.id where " \
            "brm.role_ref in %s and bm.pid='0' group by bm.id,bm.name,bm.is_last,bm.pid,bm.url order by bm.create_date"%(rids)
        rows=getSelectSql(sql)

        menu=[]
        for r in rows:
            s_menu_list=[]
            pid=r.id
            f_menu_dic = {
                "title": r.name,
                "icon": "fa-cubes",
            }
            sql="select bm.id,bm.name,bm.is_last,bm.pid,bm.url from bj_menu bm where bm.pid='%s'"%(pid)
            sub_menus=getSelectSql(sql)

            for s in sub_menus:
                s_menu_dic ={
                        "spread": True,
                        "title": s.name,
                        "icon": "fa-table",
                        "href": s.url
                        }
                s_menu_list.append(s_menu_dic)
            if len(s_menu_list)>0:
                f_menu_dic["children"]=s_menu_list
            else:
                f_menu_dic["href"]=r.url
            menu.append(f_menu_dic)

        return json.dumps(menu, ensure_ascii=False)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp



@app.route('/applymanager/vidio', methods=['GET'])
def applymanager_vidio():
    try:
        resp= render_template('video.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp
