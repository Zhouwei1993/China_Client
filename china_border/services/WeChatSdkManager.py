# -*- coding: utf-8 -*-

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# 每一个学校可以对应各自的微信企业号,由本实例进行管理
# 邮件:zwzhang@ming-china.cn
# 手机：13967374138
# 作者：'zzw'
# 公司网址： wwww.ming-jx.cn
# Copyright 嘉兴明远云服科技有限公司 2012-2016 SMT
# 日期：2016-08-10
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import china_border
import traceback
from china_border import server,info,WC_SDK_BASE
class WeChatSdkManager():

    def __init__(self):
        """
        所有学校的企业号连接对象池  WC_SDK_BASE.py
        存储方式:key:school.id ,value:weixin_sdk实例
        """
        self._wechatPools = {}

        #TODO 读取系统中的所有edu.base.school数据
        #TODO 为每一个学校实例化一个微信企业号结果对象
        ids=server.execute(info['db'], 1, info['password'], 'zdk.app', 'search', [('id', '>',0)])
        schools=server.execute(info['db'],1,info['password'],'zdk.app','read',ids,
                               ['secret','agentid'])
        for school in schools:
            self._wechatPools[school['id']] =WC_SDK_BASE.WechatQy(appid="ww7221f4e71c9f766d",
                                          appsecret=school['secret'],
                                          agentid=school['agentid'],
                                          )

    def getWc_Sdk(self,schoolid):
        """
        根据学校id获取该学校的微信接口
        :param schoolid:
        :return:
        """
        try:
            wcsdk = self._wechatPools[schoolid]
            return wcsdk
        except Exception as e:
            exstr = traceback.format_exc()
            print (exstr)
            raise


