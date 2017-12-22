from china_border import wcmgr,updateSql
import json,time
ISOTIMEFORMAT='%Y-%m-%d %X'
def downloadimg():
    re=wcmgr.getWc_Sdk(6).get_departmentuserdetailinfo(1,1,1)
    userlist= json.loads(re.text)['userlist']
    mytime=time.strftime( ISOTIMEFORMAT, time.localtime() )
    for user in userlist:
        isql="update zdk_user set head_url='%s' where phone='%s'"%(user['avatar'],user['mobile'])
        updateSql(isql)
    logsql="insert into zdk_log(sendmsg,recmsg) values('%s','微信头像同步成功')"%(mytime)
    updateSql(logsql)
    print('微信头像同步成功')
def remind():
    print('remind')