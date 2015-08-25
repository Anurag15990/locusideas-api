__author__ = 'anurag'
__author__ = 'anurag'

from flask import Flask, g, redirect
from designer import settings
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from pymongo import MongoClient
import sys
from designer.services.utils import setup_context, login_user_session
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import flask_admin
from flask.ext.admin import AdminIndexView, expose

import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(settings.TEMPLATE_FOLDER))


engine = MongoEngine()


sys.setrecursionlimit(10000)

flaskapp = Flask(__name__, static_folder='../assets', template_folder='../webapps/')
flaskapp.jinja_env.add_extension('jinja2.ext.loopcontrols')
assets = Environment(flaskapp)
flaskapp.jinja_env.cache = {}
engine.init_app(flaskapp)
from designer.models.extra.session import MongoSessionInterface
flaskapp.session_interface = MongoSessionInterface(db='designerHub')

flaskapp.config['MONGODB_SETTINGS'] = {
    'db': settings.MONGODB_DB,
    'host': settings.MONGODB_HOST,
    'port': settings.MONGODB_PORT
}

client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = client.designerHub


api = MongoRest(flaskapp)

if settings.USE_CDN:
    botoConnection = S3Connection(settings.AWSAccessKeyId, settings.AWSSecretKey)
    bucket = botoConnection.get_bucket('designerzone')
    bucket_key = Key(bucket)

def start_app():
    global admin

    class MyAdminIndexView(AdminIndexView):

        @expose('/')
        def index(self):
            if not (hasattr(g, 'user') and g.user is not None and 'Admin' in g.user.roles):
                return redirect('/')
            return super(MyAdminIndexView, self).index()

start_app()
from designer.views import *


