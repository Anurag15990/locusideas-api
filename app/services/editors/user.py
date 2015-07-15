__author__ = 'anurag'

from app.services.editors import NodeEditor
from app.models.user import User, Designer
import zope

class UserEditor(NodeEditor):

    def _invoke(self):
        if self.command == 'edit-profile':
            edit_profile(self.node, self.data)
        elif self.command == 'register':
            register(self.data)
        elif self.command == 'edit-role':
            edit_role(self.action, self.node, self.message['role'])





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
    email, password = data['email'], data['password']
    if User.objects(email__iexact=email).first() is not None:
        raise Exception('User already exists')

    user = User.objects(email__iexact=email).first()
    if not User:
        user.create(name=data['name'], email=data['email'], roles=['Basic User'])
    user.password = data['Password']
    user.save()
    return user

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


class DesignerEditor(NodeEditor):

    def _invoke(self):
        if self.command == 'register-designer-profile':
            create_designer_profile(self.node, self.data)
        if self.command == 'add-my-work':
            edit_my_work(self.action, self.node, self.data)
        if self.command == 'update-bio':
            update_bio(self.node, self.data)
        if self.command == 'update-institution':
            update_institution(self.node, self.data)


def create_designer_profile(user, data):
   node = Designer.objects(user__iexact=user).first()
   if node is not None:
       raise Exception('Designer already exists')
   else:
       node = Designer.create(user=user, bio=data['bio'], institution=data['institution'], experience=data['experience'])
   node.save()
   return node


def edit_my_work(action, user, data):
    node = Designer.objects(pk=user).first()
    if action == 'add':
        node.myWorks.append(data['myWork'])
    elif action == 'remove':
        node.myWorks.remove(data['myWork'])
    else:
        print("Invalid Action")
    node.save()
    return node

def update_bio(user, data):
    node = Designer.objects(pk=user).first()
    node.bio = data['Bio']
    node.save()
    return node

def update_institution(user, data):
    node = Designer.objects(pk=user).first()
    node.institution = data['Institution']
    node.save()
    return node

def update_experience(user, data):
    node = Designer.objects(pk=user).first()
    node.experience = data['Experience']
    node.save()
    return node



