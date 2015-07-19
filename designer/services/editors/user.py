__author__ = 'anurag'

from designer.services.editors.base import BaseEditor
from designer.models.user import User
from designer.models import EmbeddedImageField
import zope

class UserEditor(BaseEditor):

    def _invoke(self):
        if self.command == 'edit-profile':
            response = edit_profile(self.node, self.data)
        elif self.command == 'register':
            response = register(self.data)
        elif self.command == 'edit-role':
            response = edit_role(self.action, self.node, self.message['role'])
        elif self.command == "update_cover":
            response = update_cover_photo(self.node, self.data)
        elif self.command == 'update-bio':
            response = update_bio(self.node, self.data)
        elif self.command == 'update-institution':
            response = update_institution(self.node, self.data)
        return response


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
        user.save()
    except Exception,e:
        raise Exception(e)
    return user

def edit_role(action, user, role):
    node = User(pk=user)
    if action == "add":
        node.roles.append(role)
    elif action == "remove":
        node.roles.remove(role)
    else:
        print "Invalid Action"
    node.save()
    return node

def update_cover_photo(user, data):
    node = User(pk=user)
    if data['image'] is not None:
        node.cover_image = EmbeddedImageField.create(data["image"])
    node.save()
    return node

def update_bio(user, data):
    node = User.objects(pk=user).first()
    node.bio = data['Bio']
    node.save()
    return node

def update_institution(user, data):
    node = User.objects(pk=user).first()
    node.institution = data['Institution']
    node.save()
    return node

def update_experience(user, data):
    node = User.objects(pk=user).first()
    node.experience = data['Experience']
    node.save()
    return node
