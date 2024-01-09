from mongoengine import *
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField, ReferenceField, ObjectId


class Tag(EmbeddedDocument):
    name = StringField()


class Authors(Document):
    name = StringField(unique=True)


class Quotes(Document):
    title = StringField(required=True)
    author = ReferenceField((Authors), dbref=ObjectId,
                            reverse_delete_rule=CASCADE, required=True)
    tags = ListField(EmbeddedDocumentField(Tag))
    meta = {'allow_inheritance': True}
