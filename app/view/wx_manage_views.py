# -*- coding:utf-8 -*-
__author__ = 'lilin'

from flask import render_template
from app import app
from app.weixin import accesstoken
from app.weixin import menu

@app.route('/menuadmin', methods=['GET', 'POST'])
def menuadmin():
    return render_template('menu.html')


# 创建菜单
@app.route('/createMenu', methods=['GET', 'POST'])
def createMenu():
    menuManager = menu.MenuManager()
    result = menuManager.create_menu(accesstoken.token)
    if result.has_key('errcode') & result.has_key('errmsg'):
        return render_template('menu.html', errcode=result['errcode'], errmsg=result['errmsg'], msg='创建菜单')
    else:
        return render_template('menu.html', result=result, msg='创建菜单')


@app.route('/getMenu', methods=['GET', 'POST'])
def getMenu():
    menuManager = menu.MenuManager()
    result = menuManager.get_menu(accesstoken.token)
    if result.has_key('errcode') & result.has_key('errmsg'):
        return render_template('menu.html', errcode=result['errcode'], errmsg=result['errmsg'], msg='查询菜单')
    else:
        return render_template('menu.html', result=result, msg='查询菜单')


@app.route('/deleteMenu', methods=['GET', 'POST'])
def deleteMenu():
    menuManager = menu.MenuManager()
    result = menuManager.delete_menu(accesstoken.token)
    if result.has_key('errcode') & result.has_key('errmsg'):
        return render_template('menu.html', errcode=result['errcode'], errmsg=result['errmsg'], msg='删除菜单')
    else:
        return render_template('menu.html', result=result, msg='删除菜单')