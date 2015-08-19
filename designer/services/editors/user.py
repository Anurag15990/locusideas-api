__author__ = 'anurag'

from designer.services.editors.base import BaseEditor, response_handler
from designer.models.user import User
from designer.models.image import UserImage
from flask import jsonify, g, session
from designer.services.utils import login_user_session
import zope

class UserEditor(BaseEditor):

    def _invoke(self):
        if self.command == 'edit-profile':
            response = edit_profile(self.node, self.data)
        elif self.command == 'register':
            response = register(self.data)
        elif self.command == 'edit-role':
            response = edit_role(self.action, self.node, self.data['role'])
        elif self.command == "update-cover":
            response = update_cover_photo(self.node, self.data)
        elif self.command == 'update-profile-photo':
            response = update_profile_photo(self.node, self.data)
        elif self.command == 'update-bio':
            response = update_bio(self.node, self.data)
        elif self.command == 'update-institution':
            response = update_institution(self.node, self.data)
        elif self.command == 'update-experience':
            response = update_experience(self.node, self.data)
        elif self.command == 'update-contact-info':
            response = update_contact_info(self.node, self.data)
        elif self.command == 'change-password':
            response = change_password(self.node, self.data)
        elif self.command == 'logout':
            response = logout()
        elif self.command == 'update-work-focus':
            response = update_work_focus(self.node,self.data)
        elif self.command == 'update-work-style':
            response = update_work_style(self.node,self.data)
        elif self.command == 'update-work-interest':
            response = update_work_interest(self.node,self.data)
        return response


@response_handler('Successfully edited Profile', 'Failed to Edit Profile')
def edit_profile(user, data):
    node = User.objects(pk=user).first()
    for k, v in data.iteritems():
        if not hasattr(node, k) or k == 'email':
            continue
        v = v.strip()
        setattr(node, k, v)
        print("K[%s] : V[%s]" %(k,v))
    node.save()
    return node

@response_handler('User Registered Successfully', 'Error occurred while Registering User', login_required=False)
def register(data):
    email, password, confirm, roles = data['email'], data['password'], data["confirm"], data['roles']
    if User.objects(email__iexact=email).first() is not None:
        raise Exception('User already exists')

    user = User.objects(email__iexact=email).first()
    if not user:
        user = User.create(name=data['name'], email=data['email'])
        if data['roles'] is None:
            user.roles = ['Basic User']
        else:
            user.roles = data['roles']
    try:
        user.change_password(confirm=confirm, password=password)

        if hasattr(data, 'address') and data['address'] is not None:
            user.address = data['address']

        if hasattr(data, 'phone') and data['phone'] is not None:
            user.phone = data['phone']

        if hasattr(data, 'mobile') and data['mobile'] is not None:
            user.mobile = data['mobile']

        user.is_verified = False
        user.admin_approved = False

        user.save()
    except Exception,e:
        raise Exception(e)
    return user

@response_handler('Successfully edited role', 'Error occurred while editing role')
def edit_role(action, user, role):
    node = User.objects(pk=user).first()
    if action == "add":
        node.roles.append(role)
    elif action == "remove":
        node.roles.remove(role)
    else:
        print "Invalid Action"
    node.save()
    return node

@response_handler('Successfully updated cover photo', 'Failed to update cover photo')
def update_cover_photo(user, data):
    if data['cover_image'] is not None:
        cover_image = data['cover_image']
        cover_Image = UserImage.set_Cover(cover_image, user=user)
    return cover_Image

def update_profile_photo(user, data):
    if data['profile_photo'] is not None:
        profile_photo = data['profile_photo']
        profile_image = UserImage.set_Profile(profile_photo, user=user)
    return profile_image

@response_handler('Successfully updated bio', 'Failed to update bio')
def update_bio(user, data):
    node = User.objects(pk=user).first()
    if data['bio'] is not None:
        node.bio = data['bio']
        node.save()
    return node

@response_handler('Successfully updated institution', 'Failed to update institution')
def update_institution(user, data):
    node = User.objects(pk=user).first()
    if data['institution'] is not None:
        node.institution = data['institution']
        node.save()
    return node

@response_handler('Successfully updated experience', 'Failed to update experience')
def update_experience(user, data):
    node = User.objects(pk=user).first()
    if data['experience'] is not None:
        node.experience = data['experience']
        node.save()
    return node

@response_handler('Successfully updated contact info', "Failed to update contact info")
def update_contact_info(user, data):
    node = User.objects(pk=user).first()
    if data['address'] is not None:
        node.address = data['address']

    if data['mobile'] is not None:
        node.mobile = data['mobile']

    if data['phone'] is not None:
        node.phone = data['phone']

    node.save()
    return node

@response_handler('Logged out successfully', 'Error Logging out')
def logout():
    if hasattr(g, 'user'):
        g.user = None
        session.clear()
        return None

@response_handler('Successfully changed password', 'Error while changing password')
def change_password(user, data):
    node = User.objects(pk=user).first()
    node.change_password(password=data['password'], confirm=data['confirm'])
    node.save()
    return node

@response_handler('Successfully updated work-focus','Error while updating work-focus',login_required=True)
def update_work_focus(user,data):
    node = User.objects(pk=user).first()
    node.work_focus = data['work-focus']
    node.save()
    return node

@response_handler('Successfully updated work-style','Error while updating work-style',login_required=True)
def update_work_style(user,data):
    node = User.objects(pk=user).first()
    node.work_style = data['work-style']
    node.save()
    return node

@response_handler('Successfully updated work-interest','Error while updating work-interest',login_required=True)
def update_work_interest(user,data):
    node = User.objects(pk=user).first()
    node.work_interest = data['work-interest']
    node.save()
    return node