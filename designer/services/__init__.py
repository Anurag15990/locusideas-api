__author__ = 'anurag'

(USER, DESIGNER) = ("user", "designer")

class NodeFactory(object):

    @classmethod
    def get_model_by_id(cls, model_class, id):
        model_name = NodeFactory.get_model_by_name(model_class)
        return model_name.get_by_id(id)


    @classmethod
    def get_model_by_name(cls, name):
        from designer.models.user import User
        name = name.lower()

        if name == USER: return User
        else: return None



