import mongoengine as me


class ModuleResponse(me.EmbeddedDocument):
    success = me.StringField(required=True)
    fail = me.StringField(required=True)


class ModuleAnswer(me.EmbeddedDocument):
    text = me.StringField(required=True)
    destination = me.IntField(required=True)


class Module(me.EmbeddedDocument):
    _id = me.ObjectIdField(required=True)
    name = me.StringField(required=True)
    position = me.IntField(required=True)
    description = me.StringField(required=True)
    response = me.EmbeddedDocumentField(ModuleResponse, required=True)
    answers = me.EmbeddedDocumentListField(ModuleAnswer)
    time_max = me.IntField(required=True)
    win_condition = me.ListField()
    _type = me.StringField(required=True)


class Story(me.Document):
    user_id = me.ObjectIdField(required=True)
    title = me.StringField(required=True)
    character_name = me.StringField(required=True)
    stage = me.IntField(required=True)
    modules = me.EmbeddedDocumentListField(Module, required=True)
    companion_name = me.StringField(required=True)
    life = me.IntField(required=True)




