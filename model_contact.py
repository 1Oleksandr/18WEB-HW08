from mongoengine import *
from mongoengine.fields import BooleanField, StringField, ObjectId


class Contacts(Document):
    email = StringField(required=True, unique=True)
    name = StringField(required=True)
    phone = StringField(unique=True)
    send_type = StringField(required=True, default='email')
    done = BooleanField(default=False)
    # meta = {'allow_inheritance': True}
