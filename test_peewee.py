# -*- coding:utf-8 -*-
__author__ = 'lilin'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, g
import MySQLdb
import setting

app = Flask(__name__)
app.debug = True


def before_request():
    g.db = MySQLdb.connect(setting.MYSQL_HOST_M, setting.MYSQL_USER, setting.MYSQL_PASS,
                           setting.MYSQL_DB, port=int(setting.MYSQL_PORT), charset='utf8')


def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()