import mongoengine as me


class User(me.Document):
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    tokens = me.ListField(null=False)
    username = me.StringField(required=True, unique=True)
    created_at = me.DateTimeField(required=True)
