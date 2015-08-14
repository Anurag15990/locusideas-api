__author__ = 'anurag'


from designer.settings import MEDIA_FOLDER
import base64
from PIL import Image, ImageFile
from flask import g, session, jsonify
import datetime, random
import os
import json, collections
from functools import wraps


PAGE_SIZE = 50


def decode_base64(data):
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'='* missing_padding
        return base64.decodestring(data)


def login_user_session(user):
    session['user'] = str(user.id)
    session['just_logged_in'] = True


def get_random():
    return random.randint(0, 999999999)


def convert_filters_to_query(filters):
    query_filters = {}
    if filters is not None and len(filters) > 0:
        for filter in filters:
            if filter.get('type') == 'list':
                inner_filter = {}
                inner_filter['$in'] = filter.get('value')
                query_filters[filter.get('name')] = inner_filter
            elif filter.get('type') == 'entity':
                query_filters[filter.get('name')] = filter.get('value')
        return query_filters


class JSONSetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, collections.Set):
            return list(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def login_required(func):

    @wraps(func)
    def decorate(*args,**kwargs):
        if hasattr(g, 'user') and g.user is not None and g.user.id is not None:
            return func(*args, **kwargs)
        else:
            return dict(status='Failure', message='Please Login before proceeding')
    return decorate

def setup_context():
    user = g.user if hasattr(g, 'user') and g.user is not None else None
    if hasattr(g, 'just_logged_in') and g.just_logged_in:
        show_message_notification = True
    else:
        show_message_notification = False
    return dict(user=user, show_message_notification=show_message_notification)