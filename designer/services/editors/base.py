__author__ = 'anurag'

from designer.app import flaskapp
from flask import jsonify, request

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
        type = message['type']
        if type is None:
            raise Exception('Invalid Message')
        if type == 'base':
            return BaseEditor(message)
        if type == 'user':
            return UserEditor(message)
        if type == 'photo':
            return ImageEditor(message)

