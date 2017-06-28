# -*- coding:utf-8 -*-
__author__ = 'lilin'
from datetime import *
import time
from flask import g, request, make_response, render_template
import hashlib
import xmltodict
from app import app
from app.weixin import accesstoken
# from app.model import signup
from app.model.signup import Signup
import urllib2
import json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    c = g.db.cursor()
    if request.method == 'GET':
        token = 'weixin'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if ( hashlib.sha1(s).hexdigest() == signature ):
            return make_response(echostr)

    # access_token
    access_token = accesstoken.token
    # print 'access_token:' + access_token
    c.execute(
        'insert into t_token(token,time) values(%s,%s)',
        [access_token, time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))])
    # message & event
    # xml_recv = ET.fromstring(request.data)
    message = xmltodict.parse(request.data)['xml']
    ToUserName = message["ToUserName"] if message.has_key('ToUserName') else ""
    FromUserName = message["FromUserName"] if message.has_key('FromUserName') else ""
    MsgType = message["MsgType"] if message.has_key('MsgType') else ""
    CreateTime = message["CreateTime"] if message.has_key('CreateTime') else ""

    response = ''
    if MsgType == 'text':
        Content = message["Content"] if message.has_key('Content') else ""
        MsgId = message["MsgId"] if message.has_key('MsgId') else ""
        print 'Content:', Content
        text(c, FromUserName, ToUserName, Content, datetime.fromtimestamp(int(CreateTime)), MsgType, MsgId)
        content = '你说啥，你再说一遍'
        response = reply_response(FromUserName, ToUserName, str(int(time.time())), content)
    if MsgType == 'event':
        Event = message["Event"] if message.has_key('Event') else ""
        EventKey = message["EventKey"] if message.has_key('EventKey') else ""
        Ticket = message["Ticket"] if message.has_key('Ticket') else ""
        print 'Event:', Event
        print 'EventKey:', EventKey
        print 'Ticket:', Ticket

        event(c, FromUserName, ToUserName, datetime.fromtimestamp(int(CreateTime)), MsgType, Event, EventKey, Ticket)

        if Event == 'subscribe':
            # 关注
            content = '此刻终于等到你！'
            response = reply_response(FromUserName, ToUserName, str(int(time.time())), content)
        if Event == 'SCAN':
            content = '你大爷的你已经关注我了!'
            response = reply_response(FromUserName, ToUserName, str(int(time.time())), content)
        if Event == 'CLICK':
            # 签到
            if EventKey == 'V1001_SIGNUP':
                class_name = '默认培训'
                picurl = 'http://ibmuec.sinaapp.com/static/images/signup.png'
                url = 'http://ibmuec.sinaapp.com/signups'
                count_you = get_count_signup_by_openid(c, FromUserName, class_name)
                user_info = get_user_info_by_openid(access_token, FromUserName)
                nickname = user_info['nickname']
                headimgurl = user_info['headimgurl']
                print 'count_you:', count_you
                if count_you < 1:
                    count_all = get_count_signup_by_class_name(c, class_name)
                    print 'count_index:', count_all + 1
                    Signup(openid=FromUserName, class_name=class_name, is_signup=1, count_index=count_all + 1,
                                  nickname=nickname, headimgurl=headimgurl).save()
                    content = nickname + ',谢谢签到！您是第' + str(count_all + 1) + '位签到的同学！'
                else:
                    count_index = get_count_index_signup_by_openid(c, FromUserName, class_name)
                    content = nickname + ',您已签到！您是第' + str(count_index) + '位签到的同学！'
                response = reply_response_with_image(FromUserName, ToUserName, str(int(time.time())), "1", "课程签到情况",
                                                     content, picurl, url)
            # 点赞
            # if EventKey == 'V1001_GOOD':
            #     content = '谢谢为我们点赞!'
            #     response = reply_response(FromUserName, ToUserName, str(int(time.time())), content)
    return response


# 保存消息
def text(cursor, fromusername, tousername, content, createtime, msg_type, msg_id):
    cursor.execute(
        'insert into t_message(fromusername,tousername,content,createtime,msg_type,msg_id) values(%s,%s,%s,%s,%s,%s)',
        [fromusername, tousername, content, createtime, msg_type, msg_id])


# 保存事件
def event(cursor, fromusername, tousername, createtime, msg_type, event, eventkey, ticket):
    cursor.execute(
        'insert into t_event(fromusername,tousername,createtime,msgtype,event,eventkey,ticket) values(%s,%s,%s,%s,%s,%s,%s)',
        [fromusername, tousername, createtime, msg_type, event, eventkey, ticket])


# openid,class_name的签到记录
def get_count_signup_by_openid(cursor, openid, class_name):
    sql = 'select count(*) as count from t_signup t where t.openid = %s and t.class_name = %s and t.is_signup = %s;'
    cursor.execute(sql, [openid, class_name, 1])
    count = cursor.fetchone()[0]
    return count


# openid,class_name的签到顺序
def get_count_index_signup_by_openid(cursor, openid, class_name):
    sql = 'select t.count_index from t_signup t where t.openid = %s and t.class_name = %s;'
    cursor.execute(sql, [openid, class_name])
    index = cursor.fetchone()[0]
    return index


# class_name的签到记录数
def get_count_signup_by_class_name(cursor, class_name):
    sql = 'select count(*) as count from t_signup t where t.class_name = %s and t.is_signup = %s;'
    cursor.execute(sql, [class_name, 1])
    count = cursor.fetchone()[0]
    return count


# 回复OPENID文本信息
def reply_response(tousername, fromusername, createtime, content):
    reply_template = "<xml><ToUserName><![CDATA[%s]]></ToUserName>" \
                     "<FromUserName><![CDATA[%s]]></FromUserName>" \
                     "<CreateTime>%s</CreateTime><MsgType><![CDATA[text]]>" \
                     "</MsgType><Content><![CDATA[%s]]></Content></xml>"
    response = make_response(reply_template % (tousername, fromusername, createtime, content))
    response.content_type = 'application/xml'
    return response


# 回复OPENID图文信息,单条
def reply_response_with_image(tousername, fromusername, createtime, articlecount, title, description, picurl, url):
    reply_template = '''<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[news]]></MsgType>
                        <ArticleCount>%s</ArticleCount>
                        <Articles>
                        <item>
                        <Title><![CDATA[%s]]></Title>
                        <Description><![CDATA[%s]]></Description>
                        <PicUrl><![CDATA[%s]]></PicUrl>
                        <Url><![CDATA[%s]]></Url>
                        </item>
                        </Articles>
                        </xml>'''

    response = make_response(
        reply_template % (tousername, fromusername, createtime, articlecount, title, description, picurl, url))
    response.content_type = 'application/xml'
    return response


def get_user_info_by_openid(access_token, openid):
    user_info_url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"
    html = urllib2.urlopen(user_info_url).read()
    return json.loads(html)