# -*- coding:utf-8 -*-
__author__ = 'lilin'

from peewee import *
import basemodel


class Question(basemodel.BaseModel):
    question = TextField()
    nickname = TextField()
    openid = TextField()
    checked = IntegerField()

    class Meta:
        db_table = 't_question'
