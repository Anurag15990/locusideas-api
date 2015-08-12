__author__ = 'anurag'

from flask import Flask, request, jsonify, render_template, session, g
import settings
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from pymongo import MongoClient
import sys
import json

sys.setrecursionlimit(10000)

flaskapp = Flask(__name__, static_folder='assets', template_folder='webapps/')
from designer.models.extra.session import MongoSessionInterface
flaskapp.session_interface = MongoSessionInterface(db='designerHub')

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

@flaskapp.before_request
def before_request():
    from designer.models.user import User
    session.permanent = True
    if session.get('user') is not None:
        g.user = User.objects(pk=session['user']).first()
    else:
        g.user = None
    if session.get('just_logged_in', False):
        g.just_logged_in = True
        session['just_logged_in'] = False



@flaskapp.route('/editors/invoke', methods=['POST'])
def editor_invoke():
    try:
        message = request.get_json(force=True)
        from designer.services.editors.base import BaseEditor
        editor = BaseEditor.factory(message)
        response = editor._invoke()
        return jsonify(response)
    except Exception, e:
        return jsonify(dict(status='error', message='Something went wrong', exception=str(e)))

@flaskapp.route('/extractors/invoke', methods=['POST'])
def extractor_invoke():
    try:
        message = request.get_json(force=True)
        from designer.services.extractors.base import BaseExtractor
        extractor = BaseExtractor.factory(message)
        response = extractor._invoke()
        return jsonify(response)
    except Exception, e:
        return jsonify(dict(status='error', message='Something went wrong', exception=str(e)))

@flaskapp.route('/user/add')
def render_template_for_user():
    try:
        return render_template('pages/index.html')
    except Exception, e:
        raise e

@flaskapp.route("/")
def render_home_template():
    try:
        return render_template('pages/home.html')
    except Exception,e:
        raise e


if __name__ == '__main__':
    flaskapp.run(host='0.0.0.0', port=4900)

