#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar,uuid
ISOTIMEFORMAT='%Y-%m-%d %X'
#用户后台管理

#用户列表1
@app.route('/applymanager/list', methods=['GET'])
@app.route('/applymanager/list/<currentpage>', methods=['GET'])
@app.route('/applymanager/list/<currentpage>/<sumpage>', methods=['GET'])
def applymanager_list(currentpage=1, sumpage=8):
    try:
        id = flask_login.current_user.id
        key = request.args.get('key')
        key_type = request.args.get('key_type')
        vcode = request.args.get('vcode')
        offset=(int(currentpage)-1)*int(sumpage)
        offset=int(offset)
        tsql="select id,sqlx,uname,cardno,mob,sqsx,create_date,flag from bj_cert where apply_count='%s'"%(id)
        countsql="select count(1) from bj_cert where apply_count='%s'"%(id)
        if key:
            tsql+=" and (uname like '%%%%%s%%%%' or danwei like '%%%%%s%%%%' or mob like '%%%%%s%%%%' or board like '%%%%%s%%%%' or car_no like '%%%%%s%%%%')"%(key,key,key,key,key)
            countsql+=" and (uname like '%%%%%s%%%%' or danwei like '%%%%%s%%%%' or mob like '%%%%%s%%%%' or board like '%%%%%s%%%%' or car_no like '%%%%%s%%%%')"%(key,key,key,key,key)
        if key_type and key_type!='0':
            tsql +=" and sqlx='%s'"%(key_type)
            countsql +=" and sqlx='%s'"%(key_type)
        tsql+="  order by id desc limit %s offset %s"%(sumpage,offset)
        trow=getSelectSql(tsql)
        countresult=getSelectSql(countsql)
        if(countresult[0][0]%sumpage==0):
            countpage=countresult[0][0]/sumpage
        else:
            countpage=countresult[0][0]/sumpage+1
        types=['登轮许可证','口岸限定区域许可证','口岸限定区域车辆通行证']
        resp= render_template('ApplyManager/List.html', basepath=BASEPATH,userlist=trow,offset=offset,countpage=countpage,currentpage=currentpage,key=key,key_type=key_type,types=types,vcode=vcode)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/sp', methods=['GET'])
def applymanager_sp():
    try:
        cid = request.args.get('cid')
        sql="select * from bj_cert where id='%s'"%(cid)
        cinfo=getSelectSql(sql)

        sql="select bu.name from bj_user bu left join bj_user_role bur on bur.user_ref=bu.id left join bj_role br on br.id=bur.role_ref where br.name='经办人'"
        jbr=getSelectSql(sql)
        sql="select bu.name from bj_user bu left join bj_user_role bur on bur.user_ref=bu.id left join bj_role br on br.id=bur.role_ref where br.name='领导'"
        ld=getSelectSql(sql)


        resp= render_template('ApplyManager/Sp.html', basepath=BASEPATH,jbr=jbr,ld=ld,cinfo=cinfo)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/add', methods=['GET'])
def applymanager_add():
    try:
        uid = flask_login.current_user.id
        sql = "select main_count from bj_company_user where id='%s'" % (uid)
        row = getSelectSql(sql)
        if row[0][0]:
            fid = row[0][0]
        else:
            fid = uid
        sql = "select id from bj_company_user where statu=2 and now()<=end_time+ '1 day' and now()>=start_time and id='%s'" % (fid)
        rows = getSelectSql(sql)
        length = len(rows)
        if length>0:
            return make_response(render_template('error.html', basepath=BASEPATH, errormsg=('此账号暂停使用！')))
        resp= render_template('ApplyManager/Add.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

@app.route('/applymanager/machine_add', methods=['GET'])
def applymanager_machine_add():
    try:
        vcode = request.args.get('vcode')
        if not vcode or vcode=='None':
            vcode=uuid.uuid1()
        resp= render_template('ApplyManager/Machine_Add.html', basepath=BASEPATH,vcode=vcode)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp

@app.route('/applymanager/machine_register', methods=['GET'])
def applymanager_machine_register():
    try:
        vcode = request.args.get('vcode')
        if not vcode or vcode=='None':
            vcode=uuid.uuid1()
        resp= render_template('ApplyManager/Machine_Register.html', basepath=BASEPATH,vcode=vcode)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/video_test', methods=['GET'])
def applymanager_video_test():
    try:
        resp= render_template('video.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/spmany', methods=['GET'])
def applymanager_spmany():
    try:
        cids = request.args.get('cids')
        cids_list=cids.split(',')
        cinfos=[]
        for c in cids_list:
            sql="select * from bj_cert where id='%s'"%(c)
            cinfo=getSelectSql(sql)
            cinfos.append(cinfo)

        sql="select bu.name from bj_user bu left join bj_user_role bur on bur.user_ref=bu.id left join bj_role br on br.id=bur.role_ref where br.name='经办人'"
        jbr=getSelectSql(sql)
        sql="select bu.name from bj_user bu left join bj_user_role bur on bur.user_ref=bu.id left join bj_role br on br.id=bur.role_ref where br.name='领导'"
        ld=getSelectSql(sql)


        resp= render_template('ApplyManager/SpMany.html', basepath=BASEPATH,jbr=jbr,ld=ld,cinfos=cinfos,cids=cids)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp





#用户删除
@app.route('/applymanager/delete/<cids>', methods=['GET'])
def applymanager_delete(cids):
    try:
       cids=cids.split(',')
       dlt=''
       for c in cids:
           #删除前每次查看是否已经审批
           sql = "select flag from bj_cert where id='%s'"%(c)
           flag=getSelectSql(sql)[0][0]
           if flag==1:
               dlt='1'
               continue
           #开始删除
           tsql="delete from bj_cert where id='%s'"%(c)
           rs=updateSql(tsql)
           if rs==1:
               continue
           else:
               return '1'
       #如果dlt为 1  则说明部分删除失败
       if dlt=='1':
           return '2'
       return '0'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp



@app.route('/applymanager/toprint/<vcode>', methods=['GET'])
def applymanager_toprint(vcode):
    try:
        resp = render_template('ApplyManager/Print.html', basepath=BASEPATH,vcode=vcode)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/go_machine', methods=['GET'])
def applymanager_go_machine():
    try:
        # vcode = request.args.get('vcode')
        # if not vcode or vcode=='None':
        #     vcode=uuid.uuid1()
        resp = render_template('ApplyManager/index.html', basepath=BASEPATH)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/user_data/<vcode>', methods=['POST'])
def applymanager_user_data(vcode):
    try:
        uinfo=[]
        sql="select * from bj_cert where vcode='%s'"%(vcode)
        rows=getSelectSql(sql)
        for r in rows:
            print(type(r.checktime))
            fdate=''
            if r.create_date:
                fdate=r.create_date.strftime('%Y-%m-%d')
            uinfo.append({
                'board':r.board,
                'uname':r.uname,
                'gender': r.gender,
                'birthday': r.birthday,
                'cardno': r.cardno,
                'address': r.address,
                'mob': r.mob,
                'ewm': r.ewm,
                'sqlx': r.sqlx,
                'danwei': r.danwei,
                'zhiwu': r.zhiwu,
                'sqsx': r.sqsx,
                'jbr': r.jbr,
                'pzbm': r.pzbm,
                'pzld': r.pzld,
                'fdate': fdate,
                'cardno_pic': r.cardno_pic,
                'car_no': r.car_no,
            })
        return json.dumps(uinfo, ensure_ascii=False)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/getuinfo/<cardno>', methods=['GET'])
def applymanager_getuinfo(cardno):
    try:
        sql="select * from bj_cert where cardno='%s' order by create_date desc limit 1"%(cardno)
        row=getSelectSql(sql)

        if len(row)>0:
            r=row[0]
            uinfo_dic={
                "uname":r.uname,
                "gender": r.gender,
                "birthday": r.birthday,
                "address": r.address,
                "mob": r.mob,
                "danwei": r.danwei,
                "cardno_pic":r.cardno_pic
            }
            return json.dumps(uinfo_dic, ensure_ascii=False)
        else:
            return '1'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp


@app.route('/applymanager/save', methods=['POST'])
def applymanager_save():
    try:
       machine_add = request.form.get('machine_add')
       if machine_add=='1':
           vcode = request.form.get('vcode')
           login_id=37
       else:
           login_id = flask_login.current_user.id
           vcode = flask_login.current_user.vcode
           print(vcode)
       ewm = request.form.get('ewm')
       sqlx = request.form.get('sqlx')
       cardno = request.form.get('cardno')
       NameA = request.form.get('NameA')
       Sex2 = request.form.get('Sex2')
       Born2 = request.form.get('Born2')
       Address = request.form.get('Address')
       mob = request.form.get('mob')
       danwei = request.form.get('danwei')
       zhiwu = request.form.get('zhiwu')
       # carno = request.form.get('carno')
       board = request.form.get('board')
       testy=request.form.get('testy')
       shiyou = request.form.get('shiyou')
       is_bhc = request.form.get('is_bhc')
       cardno_pic = request.form.get('cardno_pic')
       mytime=time.strftime( ISOTIMEFORMAT, time.localtime() )
       id = request.form.get('id')
       if id:
           sql = "select flag from bj_cert where id='%s'"%(id)
           flag=getSelectSql(sql)[0][0]
           if flag=='2':
               return '2'
           tsql=""
       else:
           if sqlx=='1':
               if is_bhc=='1':
                   board='本航次'
                   testy=''
               tsql = "insert into bj_cert(uname,gender,birthday,cardno,address,board,ewm,sqlx,zhiwu,sqsx,shiyou,flag,vcode,cardno_pic,apply_count,create_date,danwei,mob) values " \
                      "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                      (NameA,Sex2,Born2,cardno,Address,board,ewm,'登轮许可证',zhiwu,testy,shiyou,'2',vcode,cardno_pic,login_id,mytime,danwei,mob)
           elif sqlx=='2':
               tsql = "insert into bj_cert(uname,gender,birthday,cardno,address,ewm,sqlx,zhiwu,sqsx,shiyou,flag,vcode,cardno_pic,apply_count,create_date,danwei,mob) values " \
                      "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                      (NameA,Sex2,Born2,cardno,Address,ewm,'口岸限定区域许可证',zhiwu,testy,shiyou,'2',vcode,cardno_pic,login_id,mytime,danwei,mob)
           elif sqlx=='3':
               tsql = "insert into bj_cert(uname,gender,birthday,cardno,address,ewm,sqlx,zhiwu,sqsx,shiyou,flag,vcode,cardno_pic,apply_count,create_date,danwei,mob) values " \
                      "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                      (NameA,Sex2,Born2,cardno,Address,ewm,'口岸限定区域车辆通行证',zhiwu,testy,shiyou,'2',vcode,cardno_pic,login_id,mytime,danwei,mob)
       rs=updateSql(tsql)
       if rs==1:
           return '0'
       else:
           return '1'
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
        print(99)
        resp = make_response(render_template('error.html', basepath=BASEPATH, errormsg=('异常,详细 (%s)' % e)))
    return resp