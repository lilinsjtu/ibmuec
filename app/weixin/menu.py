# -*- coding:utf-8 -*-
__author__ = 'lilin'

import urllib2
import json
# import settingsae


class MenuManager:
    createMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
    deleteMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
    getMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="

    APPID = "wx7cda32a4b5369e90"
    SECRET = "1de3f779cd533a80c136b3c409f35b6c"
    redirect_uri = "http%3A%2F%2Fibmuec.sinaapp.com%2Fanswers"
    state = "123"
    # scope = "snsapi_base"
    scope = "snsapi_userinfo"
    auth_ask_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+APPID+"&redirect_uri="+redirect_uri + "&response_type=code&scope="+scope+"&state="+state+"#wechat_redirect"
    values = '''{
     "button":[
     {
          "type":"click",
          "name":"课程签到",
          "key":"V1001_SIGNUP"
      },
      {
           "name":"课程答疑",
           "sub_button":[
            {
               "type":"view",
               "name":"提问",
               "url": "'''+auth_ask_url+'''"
            }]
       }]
    }'''

    def create_menu(self, accessToken):
        result = self.sendRequest(self.createMenuUrl + accessToken, self.values)
        return result

    def get_menu(self, accessToken):
        result = self.sendRequest(self.getMenuUrl + accessToken)
        return result

    def delete_menu(self, accessToken):
        result = self.sendRequest(self.deleteMenuUrl + accessToken)
        return result

    # 发送请求，返回dict
    def sendRequest(self, url, values=None):
        print 'url:', url
        print 'values:', values
        if values:
            print "values:", values
            # data = urllib.urlencode(values)
            req = urllib2.Request(url, values)
        else:
            req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        print 'result:', result
        return result