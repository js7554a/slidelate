#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from os import path

class Config(object):
    DEBUG = False
    PORT = 5000
    HOST = '0.0.0.0'
    URL_PREFIX = '/api'
    PROJECT_ROOT = path.abspath(path.dirname(__file__))
    TEMPLATE_FOLDER = path.join(PROJECT_ROOT, 'templates')
    UPLOAD_FOLDER = path.join(PROJECT_ROOT, 'application/media/photos')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://jsilva:jx3t2016@localhost/slidelate'

class Development(Config):
    DEBUG = True
    SECRET_KEY = os.urandom(24)



class Production(Config):
	SECRET_KEY = 'production'
	try:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	except KeyError:
		pass


class Testing(Config):
    TESTING = True
    SECRET_KEY = 'testing'