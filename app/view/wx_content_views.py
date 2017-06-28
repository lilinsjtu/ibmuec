# -*- coding:utf-8 -*-
__author__ = 'lilin'

from flask import render_template, request, redirect, url_for, session
from app import app
from app.model.question import Question
from app.model.answer import Answer
from app.model.signup import Signup
import urllib2
import json
from app.weixin import accesstoken
# from wx_init_views import get_user_info_by_openid

APPID = "wx7cda32a4b5369e90"
SECRET = "1de3f779cd533a80c136b3c409f35b6c"

# 问题列表，需要获取用户信息，回调函数
@app.route('/answers', methods=['GET', 'POST'])
def answers():
    code = request.args.get('code', '')
    print "code:", code
    access_token = ''
    openid = ''
    nickname = ''
    headimgurl = ''
    if code:
        access_token_info_dict = get_auth_access_token_dict(code)
        print 'access_token_info_dict:', access_token_info_dict
        if access_token_info_dict.has_key('access_token'):
            access_token = access_token_info_dict['access_token']
            session['access_token'] = access_token
        if access_token_info_dict.has_key('refresh_token'):
            refresh_token = access_token_info_dict['refresh_token']
            print "refresh_token from wx:", refresh_token
        if access_token_info_dict.has_key('openid'):
            openid = access_token_info_dict['openid']
            session['openid'] = openid
        if access_token_info_dict.has_key('scope'):
            scope = access_token_info_dict['scope']
            print "scope from wx:", scope
        print "access_token from wx:", access_token
        print "openid from wx:", openid
    else:
        if 'access_token' in session:
            access_token = session['access_token']
            print "access_token in session:", access_token
        if 'openid' in session:
            openid = session['openid']
            print "openid in session:", openid
    if access_token:
        # 自己的信息
        print 'access_token', access_token
        print 'accesstoken.token', accesstoken.token
        if access_token != accesstoken.token:
            access_token = accesstoken.token
        user_info = get_user_info_by_openid(access_token, openid)
        print "user_info:", user_info
        nickname = user_info['nickname']
        headimgurl = user_info['headimgurl']
        print "nickname:", nickname
        print "headimgurl:", headimgurl
        session['nickname'] = nickname
        session['headimgurl'] = headimgurl
    count = Question.select().count()
    question_list = Question.select().order_by(Question.create_time.desc())
    return render_template('answer.html', question_list=question_list, count=count, nickname=nickname,
                           headimgurl=headimgurl, openid=openid)

# 保存问题，之后跟用户openid关联
@app.route('/save_question', methods=['GET', 'POST'])
def save_question():
    print "nickname:", request.form['nickname']
    q = Question(question=request.form['question'], nickname=request.form['nickname'], openid=request.form['openid'])
    q.save()
    return redirect(url_for('answers'))

# 获取access_token字典,得到openid
def get_auth_access_token_dict(code):
    access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + APPID + "&secret=" + SECRET + "&code=" + code + "&grant_type=authorization_code"
    print "access_token_url:", access_token_url
    response = urllib2.urlopen(access_token_url)
    html = response.read()
    return json.loads(html)

# 浏览单个问题,添加答案
@app.route('/view_question', methods=['GET', 'POST'])
def view_question():
    access_token = ''
    openid = ''
    nickname = ''
    headimgurl = ''
    if 'access_token' in session:
        access_token = session['access_token']
        nickname = session['nickname']
        headimgurl = session['headimgurl']
    if 'openid' in session:
        openid = session['openid']
    qid = request.args.get('question_id', '')
    q = Question.get(id=int(qid))
    return render_template('question.html', question=q, nickname=nickname,
                           headimgurl=headimgurl, openid=openid)


# 保存答案
@app.route('/save_answer', methods=['GET', 'POST'])
def save_answer():
    qid = request.form['question_id']
    q = Question.get(id=int(qid))
    a = Answer(owner=q, answer=request.form['answer'], nickname=request.form['nickname'], openid=request.form['openid'])
    a.save()
    return redirect(url_for('answers'))

# 签到情况
@app.route('/signups', methods=['GET', 'POST'])
def signups():
    access_token = accesstoken.token
    print 'access_token', access_token
    s = Signup.select().order_by(Signup.count_index)
    for ss in s:
        user_info = get_user_info_by_openid(access_token, ss.openid)
        print 'user_info', user_info
        print 'ss.id', ss.id
        print user_info.keys()
        print user_info.has_key('nickname')
        if user_info.has_key('nickname'):
            if user_info.has_key('headimgurl'):
                nickname = user_info['nickname']
                headimgurl = user_info['headimgurl']
                print 'nickname', nickname
                print 'headimgurl', headimgurl
                Signup.update(nickname=nickname, headimgurl=headimgurl).where(Signup.id==ss.id).execute()
    s = Signup.select().order_by(Signup.count_index)
    return render_template('signup.html', s=s)

# 数据库表管理
@app.route('/db', methods=['GET', 'POST'])
def db():
    return render_template('db.html')


# 创建数据库表
@app.route('/create_db', methods=['GET', 'POST'])
def create_db():
    Question.create_table(fail_silently=True)
    Answer.create_table(fail_silently=True)
    Signup.create_table(fail_silently=True)
    return redirect(url_for('db'))


# 获取用户基本信息userinfo字典（没有授权，获取的信息少），返回JSON格式
def get_user_info_by_openid(access_token, openid):
    user_info_url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"
    html = urllib2.urlopen(user_info_url).read()
    return json.loads(html)

# 获取用户基本信息userinfo字典(授权，获取的信息更多)，返回JSON格式
def get_user_info_dict(access_token, openid):
    user_info_url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"
    html = urllib2.urlopen(user_info_url).read()
    return json.loads(html)