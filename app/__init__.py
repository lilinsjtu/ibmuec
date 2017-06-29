# -*- coding:utf-8 -*-
__author__ = 'lilin'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, g
from flask_peewee.db import Database
import MySQLdb
import setting
# import settingsae
from peewee import *

app = Flask(__name__)

app.debug = True
# app.template_folder = setting.TEMPLATE_FOLDER
# app.static_folder = setting.STATIC_PATH

# PEEWEE数据库配置，从配置文件DATABASE读取
# app.config.from_object(__name__)
app.config.from_pyfile('setting.py')
# app.config.from_pyfile('settingsae.py')
db = Database(app)
# MySQLDatabase


@app.before_request
def before_request():
    g.db = MySQLdb.connect(setting.MYSQL_HOST_M, setting.MYSQL_USER, setting.MYSQL_PASS,
                           setting.MYSQL_DB, port=int(setting.MYSQL_PORT), charset='utf8')
    # g.db = MySQLdb.connect(settingsae.MYSQL_HOST_M, settingsae.MYSQL_USER, settingsae.MYSQL_PASS,
    #                        settingsae.MYSQL_DB, port=int(settingsae.MYSQL_PORT), charset='utf8')


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


import view
