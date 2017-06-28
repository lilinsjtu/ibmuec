__author__ = 'lilin'
from peewee import *
import basemodel
import question


class Answer(basemodel.BaseModel):
    owner = ForeignKeyField(question.Question, related_name='answers')
    answer = TextField()
    nickname = TextField()
    openid = TextField()
    checked = IntegerField()

    class Meta:
        db_table = 't_answer'