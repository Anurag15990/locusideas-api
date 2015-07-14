__author__ = 'anurag'



class NodeEditor(object):

    def __init__(self, message):
        self.message = message
        self.command = message.get('command', None)
        self.action = message.get('action', None)
        self.data = message.get('data', None)
        self.node = message.get('node', None)
        self.type = message.get('node', None)

    @classmethod
    def factory(cls, message):
        type = message['type']
        if type is None:
            raise Exception('Invalid Message')
        if type is 'base':
            return NodeEditor(message)