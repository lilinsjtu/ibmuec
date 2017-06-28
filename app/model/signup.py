# -*- coding:utf-8 -*-
__author__ = 'lilin'

from peewee import *
import basemodel


class Signup(basemodel.BaseModel):
    openid = TextField()
    class_name = TextField()
    is_signup = IntegerField()
    count_index = IntegerField()
    nickname = TextField()
    headimgurl = TextField()

    class Meta:
        db_table = 't_signup'
