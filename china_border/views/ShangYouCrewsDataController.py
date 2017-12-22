#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for,updateSql
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
from werkzeug.utils import secure_filename
ISOTIMEFORMAT='%Y-%m-%d %X'


#船员信息接口
@app.route('/getdatacrews', methods=['POST'])
def get_data_crews():
    #字段列表
    list = ['TRACEUNID','INSPECTTYPE','SAILORORPASSENGER','NAME','GENDER','ALIAS','SAILORDUTYID',
            'COUNTRYID','BIRTHDAY','CERTIFICATEID','CERTIFICATEUNID','PERSONCLASSID','VISACLASSID',
            'PICTURE','EFFECTS','NATIONALITYID','DISTRICTID','STATE','CREATETIME','ENAME','IMO',
            'FDIORGANID','REMARK','EXITFIRST','CUSTOMCODE','GOORFROMCOUNTRYID','IMMIGRATIONMATTERID',
            'TRANSACTSTATUS','FLAG','SECONDNAME','SECONDTYPE','SECONDCID','SECONDBIRTHDAY','SORT',
            'ISDEL','TRANRPNTSTATUS']
    # 得到发送过来的json数据并处理
    try:
        b_json = request.get_data()
        data = b_json.decode()
        json_data = json.loads(data)
    except Exception as e:
        return "1"

    # 找到UNID,OPERATION字段
    try:
        unid = json_data["UNID"]
        operation = json_data["OPERATION"]
    except Exception as e:
        return "2"

    try:
        # 判断operation的操作
        if operation == "INSERT":
            if in_sql(unid):
                return "3"
            else:
                insert_unid(unid)
                insert_all(json_data, list)
                return "0"
        if operation == "UPDATE":
            if in_sql(unid):
                insert_all(json_data, list)
                return "0"
            else:
                return "4"
        if operation == "DELETE":
            if in_sql(unid):
                delete(unid)
                return "0"
            else:
                return "4"
    except Exception as e:
        return "5"


# 判断UNID是否在数据库中,已在数据库中返回1，不在数据库中返回0
def in_sql(unid):
    print(1)
    Unsql = "select * from bj_crews where \"UNID\"='%s'" % (unid)
    Unsqlvalue = getSelectSql(Unsql)
    if len(Unsqlvalue) > 0:
        return 1
    else:
        return 0


# 在数据库中加入UNID字段
def insert_unid(unid):
    print(2)
    sql = 'insert into bj_crews ("UNID") values (\'%s\')' % (unid)
    rs = updateSql(sql)


# 将每个字段都更新到数据库中
def insert_all(json_data, list):
    print(3)
    for x in json_data:
        if x in list:
            value = json_data[x]
            sql = 'update bj_crews set "%s"=\'%s\' where "UNID"=\'%s\'' % (x, value, json_data["UNID"])
            rf = updateSql(sql)


# 删除某行
def delete(unid):
    print(4)
    sql = 'delete from bj_crews where "UNID"=\'%s\'' % (unid)
    rf = updateSql(sql)