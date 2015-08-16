__author__ = 'anurag'

from designer.app import flaskapp
from flask import jsonify, request, g
import json
from designer.services.utils import setup_context
def response_handler(success, failure, login_required=True):
    def wrap(f):
        def wrapped_f(*kargs, **kwargs):
            if login_required:
                if not hasattr(g, 'user') or g.user is None or not hasattr(g.user, 'id') or g.user.id is None:
                    return dict(status='error', message='Please login before making requests')
            try:
                node = f(*kargs, **kwargs)
                return dict(status='success', message=success, node=node, context=setup_context())
            except Exception, e:
                return dict(staus='error', message=failure, exception=str(e))
        return wrapped_f
    return wrap

class BaseEditor(object):

    def __init__(self, message):
        self.message = message
        self.command = message.get('command', None)
        self.action = message.get('action', None)
        self.data = message.get('data', None)
        self.node = message.get('node', None)
        self.type = message.get('node', None)

    def _invoke(self):
        print("Sub classes must implement this method")

    @classmethod
    def factory(cls, message):
        from designer.services.editors.user import UserEditor
        from designer.services.editors.image import ImageEditor
        from designer.services.editors.creatives import CreativesEditor
        type = message['type']
        if type is None:
            raise Exception('Invalid Message')
        if type == 'base':
            return BaseEditor(message)
        if type == 'user':
            return UserEditor(message)
        if type == 'photo':
            return ImageEditor(message)
        if type == 'creatives':
            return CreativesEditor(message)

