# -*- coding: utf-8 -*-
import time
import urllib.parse
def extime_formatstr(str):
    _s = time.mktime(time.strptime(str, '%Y-%m-%d %H:%M:%S'))
    _now = time.time()
    time_val = _now - _s
    time_val = int(time_val)
    return str
    if time_val < 60 and time_val >= 0:
        return u"刚刚"
    elif time_val >= 60 and time_val < 3600:
        return u"%i分钟前" % (time_val / 60)
    elif time_val >= 3600 and time_val < 3600 * 24:
        return u"%i小时前" % (time_val / 3600)
    elif time_val >= 3600 * 24 and time_val < 3600 * 24 * 30:
        return u"%i天前" % (time_val / 3600 / 24)
    elif time_val >= 3600 * 24 * 30 and time_val < 3600 * 24 * 30 * 12:
        return u"%i个月前"(time_val / 3600 / 24 / 30)
    elif time_val >= 3600 * 24 * 30 * 12:
        return u"%i年前"(time_val / 3600 / 24 / 30 / 12)
    else:
        return u"刚刚"



def get_now_yyyymmdd():
    ISOTIMEFORMAT='%Y-%m-%d %H:%M'
    return str(time.strftime( ISOTIMEFORMAT, time.localtime()))


def genWeiXinUrl(request,url_str):
    """
    因为腾讯的URL在不同的场景下(直接点击、转发朋友圈、转发朋友)会有不同的参数
    本函数自动从http参数列表中取出所有参数,组成正确的url
    ----->本函数只支持不带参数的业务URL<------
    :param request: flask的request对象
    :param url_str: 应用的url
    :return:
    """
    #定义意的参数一定要自己写，TX的参数可以按字典排序取出，否则签名出错
    _url = url_str
    requestParamsDict = request.args.to_dict()
    #del requestParamsDict["id"]
    requestParamsDict = sorted(requestParamsDict)
    argsLen = len(requestParamsDict)

    if argsLen > 0 :
        _url = _url + "?"
        for paramName in requestParamsDict:
            _url = _url + paramName+"="+urllib.parse.quote_plus(request.args.get(paramName))
            if argsLen > 1:
                _url = _url + "&"
                argsLen = argsLen - 1
    return _url