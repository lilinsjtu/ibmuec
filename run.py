__author__ = 'lilin'

from app import app
from app.model import question, answer

if __name__ == '__main__':
    question.Question.create_table(fail_silently=True)
    answer.Answer.create_table(fail_silently=True)
    app.debug = True
    app.run()