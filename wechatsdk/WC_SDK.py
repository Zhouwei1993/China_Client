# -*- coding: utf-8 -*-


import requests
import json
from threading import Timer
import logging
from .exceptions import ParseError, NeedParseError, NeedParamError, OfficialAPIError
from .reply import TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, Article, ArticleReply
from .lib import disable_urllib3_warning, XMLStore
from .messages import MESSAGE_TYPES, UnknownMessage
import urllib.request, urllib.parse,time,uuid
from wechatsdk.utils import WeChatSigner
import threading,xmlrpc.client

class WechatQy(object):
     timer_interval=60*60*1

     def getAPPID(self):
        return self.__appid

     def getToken(self):
        return self.__access_token
     def get_users_dic(self):
         return self.__udic

     def updateticket(self):
        t=Timer(self.timer_interval,self.updateticket)
        t.start()
        self.grant_token()
        self.grant_teticket()
        self.grant_contact_ticket()

        logging.info("已刷新ticket！")

     def genWxConf(self,url,debug):
        timestamp = int(time.time())
        noncestr = uuid.uuid1()

        #print("getSignature>nocestr:%s,ticket%s,timestamp:%s,url:%s"%(noncestr,self.__ticket,timestamp,url))
        signature = self.get_jsapi_signature(noncestr,self.__ticket,timestamp,url)
        #print("getSignature result:%s"%signature)

        jscode = "wx.config({debug:%s," \
                 "appId: '%s'," \
                 "timestamp: '%s'," \
                 "nonceStr: '%s'," \
                 "signature: '%s'," \
                 "jsApiList: [ 'checkJsApi','onMenuShareTimeline','openEnterpriseChat','onMenuShareAppMessage'," \
                 "'onMenuShareQQ','onMenuShareWeibo','hideMenuItems','showMenuItems','hideAllNonBaseMenuItem'," \
                 "'showAllNonBaseMenuItem','translateVoice','startRecord','stopRecord','onRecordEnd','playVoice'," \
                 "'pauseVoice','stopVoice','uploadVoice','downloadVoice','chooseImage','previewImage','uploadImage'," \
                 "'downloadImage','getNetworkType','openLocation','getLocation','hideOptionMenu','showOptionMenu'," \
                 "'closeWindow','scanQRCode','chooseWXPay','openProductSpecificView','addCard','chooseCard'," \
                 "'openCard','openEnterpriseContact']});"%(debug,self.__appid,timestamp,noncestr,signature)

        return jscode

     def check(self,name,szd,job,status,dict_val):

        if status!='':
            if dict_val['status']!=status:
                return 0
        if name!='':
            if str(dict_val['name']).find(name)<0:
                return 0
        if szd!='':
            if dict_val['szd']!=szd:
                return 0
        if job!='':
            if dict_val['job']!=job:
                return 0
        return 1

     def search(self,name='',szd='',job='',status=''):
        val_list=self._udic
        search_list=[]
        for value in val_list:
            dict_val=value['linkman']
            if self.check(name,szd,job,status,dict_val):
                search_list.append(value)
        return search_list

     def searchById(self,id=''):
        val_list=self._udic
        for value in val_list:
            dict_val=value['linkman']
            dict_val_id=value['id']
            if dict_val_id == id:
                return dict_val
        return False

     def searchByResUserId(self,id=''):
        val_list=self._udic
        for value in val_list:
            dict_val=value['linkman']
            if dict_val["ref_userid"][0] == int(id):
                return dict_val
        return False

     def searchByWxId(self,id=''):
        val_list=self._udic
        for value in val_list:
            dict_val=value['linkman']
            if dict_val["wxuserid"] == id:
                return dict_val
        return False

     def searchByMobile(self,id=''):
        val_list=self._udic
        for value in val_list:
            dict_val=value['linkman']
            if dict_val["phone"] == id:
                return dict_val
        return False

     def get_contact_ticket(self,url):
        nonceStr=uuid.uuid1()
        timestamp = int(time.time())
        signature=self.get_jsdept_signature(self.__group_ticket,nonceStr,timestamp,url)
        response_json={"groupId":str(self.__group_id),"timestamp":str(timestamp),"nonceStr":str(nonceStr),"signature":signature}
        print("group_id: %s timestamp: %s nonceStr: %s signature: %s"%(self.__group_id,str(timestamp),str(nonceStr),signature))
        return  response_json

     def get_jsapi_signature(self, noncestr, ticket, timestamp, url):
        data = [
            'noncestr={noncestr}'.format(noncestr=noncestr),
            'jsapi_ticket={ticket}'.format(ticket=ticket),
            'timestamp={timestamp}'.format(timestamp=timestamp),
            'url={url}'.format(url=url),
        ]
        signer = WeChatSigner(delimiter=b'&')
        signer.add_data(*data)
        return signer.signature

     def get_jsdept_signature(self,group_ticket, noncestr, timestamp, url):
        data = [
            'group_ticket={group_ticket}'.format(group_ticket=group_ticket),
            'noncestr={noncestr}'.format(noncestr=noncestr),
            'timestamp={timestamp}'.format(timestamp=timestamp),
            'url={url}'.format(url=url),
        ]
        signer = WeChatSigner(delimiter=b'&')
        signer.add_data(*data)
        return signer.signature

     def getAESKey(self):
         return self.__aeskey

     def getAgentid(self):
         return self.__agentid

     def getBacktoken(self):
         return self.__backtoken

     def __init__(self, appid=None, appsecret=None,agentid=None,backtoken=None,AESKey=None):
        self.__appid = appid
        self.__appsecret = appsecret
        self.__agentid =agentid
        self.__backtoken=backtoken
        self.__aeskey=AESKey
        self.updateticket()

        t=Timer(self.timer_interval,self.updateticket)
        t.start()

     def gen_auth_url(self,inurl=None):

         _encodeurl = urllib.request.quote(inurl,'utf-8')
         _url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s' \
                '&redirect_uri=%s&response_type=CODE&scope=snsapi_base&state=STATE#wechat_redirect' \
                ''%(self.__appid,_encodeurl)
         return _url

     def getuserid(self,code=None):
        """
        获取 userinfo
        :return: UserId
        """
        response_json = self._get(
            url="https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo",
            params={
                "access_token": self.__access_token,
                "code": code,
            }
        )
        jsondata = str(response_json, encoding = "utf-8")

        try:
            UserId = json.loads(jsondata)['UserId']
        except Exception:
            raise ParseError()

        return UserId


     def grant_teticket(self):
        """
        获取 teticket
        :return: 返回的 JSON 数据包
        """
        response_json = self._get(
            url="https://qyapi.weixin.qq.com/cgi-bin/get_jsapi_ticket",
            params={
                "access_token": self.__access_token,
            }
        )
        jsondata = str(response_json, encoding = "utf-8")
        self.__ticket = json.loads(jsondata)['ticket']

        return response_json

     def grant_contact_ticket(self):
        """
        获取 teticket
        :return: 返回的 JSON 数据包
        """
        response_json = self._get(
            url="https://qyapi.weixin.qq.com/cgi-bin/ticket/get",
            params={
                "access_token": self.__access_token,
                "type":"contact",
            })
        jsondata = str(response_json, encoding = "utf-8")
        self.__group_id = json.loads(jsondata)['group_id']
        self.__group_ticket = json.loads(jsondata)['ticket']

        return response_json

     def grant_token(self, override=True):
        """
        获取 Access Token
        详情请参考 http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        :return: 返回的 JSON 数据包
        """
        response_json = self._get(
            url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
            params={
                "corpid": self.__appid,
                "corpsecret": self.__appsecret,
            }
        )
        jsondata = str(response_json, encoding = "utf-8")
        self.__access_token = json.loads(jsondata)['access_token']
        #print(self.__access_token)
        return response_json


     def _request(self, method, url, **kwargs):
        """
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": self.__access_token,
            }

        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"],ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )

        r.raise_for_status()
        return r.content

     def _get(self, url, **kwargs):
        """
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="get",
            url=url,
            **kwargs
        )

     def _post(self, url, **kwargs):
        """
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="post",
            url=url,
            **kwargs
        )

     def _transcoding(self, data):
        """
        编码转换
        :param data: 需要转换的数据
        :return: 转换好的数据
        """
        if not data:
            return data

        result = None
        if isinstance(data, str) and hasattr(data, 'decode'):
            result = data.decode('utf-8')
        else:
            result = data
        return result

     def _transcoding_list(self, data):
        """
        编码转换 for list
        :param data: 需要转换的 list 数据
        :return: 转换好的 list
        """
        if not isinstance(data, list):
            raise ValueError('Parameter data must be list object.')

        result = []
        for item in data:
            if isinstance(item, dict):
                result.append(self._transcoding_dict(item))
            elif isinstance(item, list):
                result.append(self._transcoding_list(item))
            else:
                result.append(item)
        return result

     def _transcoding_dict(self, data):
        """
        编码转换 for dict
        :param data: 需要转换的 dict 数据
        :return: 转换好的 dict
        """
        if not isinstance(data, dict):
            raise ValueError('Parameter data must be dict object.')

        result = {}
        for k, v in data.items():
            k = self._transcoding(k)
            if isinstance(v, dict):
                v = self._transcoding_dict(v)
            elif isinstance(v, list):
                v = self._transcoding_list(v)
            else:
                v = self._transcoding(v)
            result.update({k: v})
        return result

     def parse_data(self, data):
        """
        解析微信服务器发送过来的数据并保存类中
        :param data: HTTP Request 的 Body 数据
        :raises ParseError: 解析微信服务器数据错误, 数据不合法
        """
        result = {}
        if type(data) == str:
             data = data.encode('utf-8')
        else:
            raise ParseError()

        try:
            xml = XMLStore(xmlstring=data)
        except Exception:
            raise ParseError()

        result = xml.xml2dict
        result['raw'] = data
        result['type'] = result.pop('MsgType').lower()

        message_type = MESSAGE_TYPES.get(result['type'], UnknownMessage)
        self.__message = message_type(result)
        self.__is_parse = True
        return result

     def send_text_message(self, user_id, content):
        agentid=self.__agentid
        """
        发送文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        print(content+ "\n   收件人帐号 "+user_id )

        t = threading.Thread(target=self.thread_send_msg,kwargs={"user_id":user_id,"content":content,"agentid":agentid})
        t.start()

     def thread_send_msg(self,user_id, content,agentid):
        _url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        self._post(
            url=_url,
            data={
                'touser': user_id,
                'msgtype': 'text',
                'agentid': agentid,
                'text': {
                    'content': content,
                }
            }
        )

     def grunt_token＿baidu(self):
        apiKey = "6cHYpwHmzbe8Tx7eTsYW0ITb"
        secretKey = "db91b5b797f60c99a58adc3377b3dd3c"

        response_json = self._get(
        url="https://openapi.baidu.com/oauth/2.0/token",
        params={
          "grant_type" : "client_credentials",
          "client_id" : apiKey,
          "client_secret" : secretKey
        })

        jsondata = str(response_json, encoding = "utf-8")
        self.__baidu＿access_token = json.loads(jsondata)['access_token']


     def ayvoice(self,mediaid):
        response_json = self._post(
            url="http://vop.baidu.com/server_api",
            data={
                "format":"amr",
                "rate":8000,
                "channel":1,
                "token":self.__baidu＿access_token,
                "cuid":str(uuid.uuid1()),
                "url":"https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(self.__access_token,mediaid),
            }
        )
        print(response_json)
        print("https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(self.__access_token,mediaid))

     def get_weixin_image(self,serverId):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(self.__access_token,serverId))

     def get_userinfo(self,userid):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s&userid=%s"%(self.__access_token,userid))

     def get_departmentuserdetailinfo(self,departmentid,fetchchild,status):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token=%s&department_id=%s&fetch_child=%s&status=%s"%(self.__access_token,departmentid,fetchchild,status))
