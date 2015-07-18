__author__ = 'anurag'

from flask import Flask, request, jsonify
import settings
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from pymongo import MongoClient
import sys
import json

sys.setrecursionlimit(10000)

flaskapp = Flask(__name__, static_folder='assets')

flaskapp.config['MONGODB_SETTINGS'] = {
    'db': settings.MONGODB_DB,
    'host': settings.MONGODB_HOST,
    'port': settings.MONGODB_PORT
}

client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = client.designerHub

engine = MongoEngine()
engine.init_app(flaskapp)

api = MongoRest(flaskapp)


@flaskapp.route('/editors/invoke', methods=['POST'])
def editor_invoke():
    try:
        message = request.get_json(force=True)
        from designer.services.editors.base import BaseEditor
        editor = BaseEditor.factory(message)
        return jsonify(status='success')
    except Exception, e:
        return jsonify(dict(status='error', message='Something went wrong', exception=str(e)))




if __name__ == '__main__':
    flaskapp.run(host='0.0.0.0', port=4900)

