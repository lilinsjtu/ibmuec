# -*- coding:utf-8 -*-
import sae
import os
import sys

root = os.path.dirname(__file__)

# 两者取其一
sys.path.insert(0, os.path.join(root, 'site-packages'))
from app import app
application = sae.create_wsgi_app(app)