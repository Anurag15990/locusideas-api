__author__ = 'anurag'

from app import engine

WISHLISTED, WISHLISTED_BY = "wishlisted", "wishlisted_by"

inverse_relation = {
    WISHLISTED : WISHLISTED_BY
}

class Relationship(engine.Document):

    subject = engine.GenericReferenceField()
    object = engine.GenericReferenceField()
    relation = engine.StringField()

    @classmethod
    def create_relationship(cls, subject, object, relation):
        if Relationship.objects(subject=subject, object=object, relation=relation).first() is None:
            relationship1 = Relationship(subject=subject, object=object, relation=relation)
            relationship1.save()
        if Relationship.objects(subject=object, object=subject, relation=inverse_relation.get(relation)).first() is None:
            relationship2 = Relationship(subject=subject, object=object, relation=inverse_relation.get(relation))
            relationship2.save()
        return relationship1, relationship2

    @classmethod
    def remove_relationship(cls, subject, object, relation):
        relationship1 = Relationship.objects(subject=subject, object=object, relation=relation).first()
        if relationship1 is not None:
            relationship1.delete()
        relationship2 = Relationship.objects(subject=object, object=subject, relation=inverse_relation.get(relation)).first()
        if relationship2 is not None:
            relationship2.delete()
        print "Removed Relations: ", relationship1 , " " , relationship2
        

    @classmethod
    def wishlist(cls, subject, object, relation):
        r1, r2 = cls.create_relationship(subject, object, relation)

    @classmethod
    def unwishlist(cls, subject, object, relation):
        cls.unwishlist(subject, object, relation)

