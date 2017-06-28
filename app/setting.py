# -*- coding=utf-8 -*-
__author__ = 'zero'

# import sae.const

# MYSQL配置信息
# 本地
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
MYSQL_HOST_M = '127.0.0.1'
MYSQL_HOST_S = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_DB = 'wechat'

# SINAAPP
# MYSQL_USER = sae.const.MYSQL_USER
# MYSQL_PASS = sae.const.MYSQL_PASS
# MYSQL_HOST_M = sae.const.MYSQL_HOST
# MYSQL_HOST_S = sae.const.MYSQL_HOST_S
# MYSQL_PORT = sae.const.MYSQL_PORT
# MYSQL_DB = sae.const.MYSQL_DB

TEMPLATE_FOLDER = 'templates'
STATIC_PATH = 'app/static'

DATABASE = {
    'name': 'wechat',
    'engine': 'peewee.MySQLDatabase',
    'user': 'root',
    'passwd': 'root',
    'charset': 'utf8'
}

# sae环境
# DATABASE = {
#     'host': sae.const.MYSQL_HOST,
#     'port': int(sae.const.MYSQL_PORT),
#     'name': sae.const.MYSQL_DB,
#     'engine': 'peewee.MySQLDatabase',
#     'user': sae.const.MYSQL_USER,
#     'passwd': sae.const.MYSQL_PASS,
#     'charset': 'utf8'
# }

Debug = True
SECRET_KEY = 'shanghai'