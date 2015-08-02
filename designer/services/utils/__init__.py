__author__ = 'anurag'


from designer.settings import MEDIA_FOLDER
import base64
from PIL import Image, ImageFile
from flask import g, session
import datetime, random
import os


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
    for filter in filters:
        if filter.get('list') is True:
            inner_filter = {}
            inner_filter['$in'] = filter.get('value')
            query_filters[filter.get('name')] = inner_filter
        elif filter.get('entity') is True:
            query_filters[filter.get('name')] = filter.get('value')
    return query_filters