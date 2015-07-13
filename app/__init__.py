__author__ = 'anurag'

from flask import Flask
import settings
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from pymongo import MongoClient

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': settings.MONGODB_DB,
    'host': settings.MONGODB_HOST,
    'port': settings.MONGODB_PORT
}

client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = client.designerHub

engine = MongoEngine()
engine.init_app(app)

api = MongoRest(app)

if __name__ == '__main__':
    app.run(host='localhost', port=4900)

