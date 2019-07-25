import mongoengine as me


class UserToken(me.EmbeddedDocument):
    token = me.StringField(required=True)
    issue = me.DateTimeField(required=True)
    lifetime = me.IntField(required=True)


class User(me.Document):
    email = me.EmailField(required=True)
    password = me.StringField(required=True)
    tokens = me.EmbeddedDocumentListField(UserToken)
    username = me.StringField(required=True)
