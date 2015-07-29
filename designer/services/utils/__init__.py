__author__ = 'anurag'


from designer.settings import MEDIA_FOLDER
import base64
from PIL import Image, ImageFile
from flask import g, session
import datetime, random
import os



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


