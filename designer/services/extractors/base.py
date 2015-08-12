__author__ = 'anurag'

from designer.services.utils import PAGE_SIZE


class BaseExtractor(object):

    def __init__(self, message):

        self.message = message
        self.type = message.get('type')
        self.page_size = (message.get('pageSize') if hasattr(message, 'pageSize') else PAGE_SIZE)
        self.filters = message.get('filters')
        self.search_Query = message.get('search_query')

    def _invoke(self):
        print "Implemented by SubClasses"

    @classmethod
    def factory(cls, message):
        from designer.services.extractors.user import UserExtractor
        type = message['type']
        if type == 'base':
            return BaseExtractor(message)
        if type == 'user':
            return UserExtractor(message)