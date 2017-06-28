# -*- coding:utf-8 -*-
__author__ = 'lilin'

import urllib2
import json
import pylibmc as memcache
from flask import g
import time

mc = memcache.Client()
token = mc.get('token')
# token = None
if token == None:
    # appid='wx6183086744659589'
    # appsecret='4c2bdadb100c57b8b85a41947a209f3c'
    appid = "wx7cda32a4b5369e90"
    appsecret = "1de3f779cd533a80c136b3c409f35b6c"
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + appsecret
    response = urllib2.urlopen(url)
    html = response.read()
    tokeninfo = json.loads(html)
    token = tokeninfo['access_token']
    # print 'TOKEN:' + token
    # c = g.db.cursor()
    # c.execute(
    #     'insert into t_token(token,time) values(%s,%s)',
    #     [token, time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))])
    mc.set('token', token, 7200)
    token = mc.get('token')
