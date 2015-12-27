__author__ = 'anurag'

from designer.app import flaskapp
from flask import session, g, request, jsonify, render_template, redirect
from designer.services.utils import login_required, login_user_session, setup_context
from designer.services.extractors.user import UserExtractor

# Function for Logging in to the mobile App.
@flaskapp.route('/mobile/login', methods=['POST'])
def mobileLogin():
    try:
        from designer.models.user import User
        message = request.get_json(force=True)
        email , password = message['email'], message['password']
        user = User.authenticate(email, password)
        if user and user.id:
            login_user_session(user)
            response = jsonify(dict(status='success', message='Successfully logged in', node=user))
            return response
        else:
            return jsonify(dict(status='error', message='Invalid EmailId and/or Password'))
    except Exception,e:
        raise e

# Function for Logging out of the mobile App.
@flaskapp.route('/mobile/logout', methods=['GET'])
def mobileLogout():
    try:
        if hasattr(g, 'user'):
            g.user = None
            session.clear()
            return jsonify(dict(status='success', message='Successfully logged out'))
    except Exception,e:
        raise e