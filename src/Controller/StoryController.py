from bson.objectid import ObjectId
from flask import (json, Response)
from mongoengine import ValidationError

from DTO.StoryDTO import StoryDTO
from Middleware.Auth import auth
from Model.Story import Story, Module, ModuleResponse, ModuleAnswer


@auth
def store(req, **kwargs):
    data = req.get_json()
    error = []

    try:
        modules = []
        for m in data['modules']:
            rs = ModuleResponse(success=m['response']['success'], fail=m['response']['fail'])

            aw = []
            if 'answers' in m:
                for answer in m['answers']:
                    aw.append(ModuleAnswer(
                        text=answer['text'],
                        destination=answer['destination']
                    ))

            mo = Module(
                _id=ObjectId(),
                name=m['name'],
                description=m['description'],
                response=rs,
                _type=m['type'],
                time_max=m['time_max'],
                position=m['position'],
                win_condition=m['win_condition'],
                answers=aw)
            modules.append(mo)

        new_story = Story(user_id=ObjectId(str(kwargs['request_user'].id)),
                          character_name=data['character_name'],
                          stage=data['stage'],
                          companion_name=data['companion_name'],
                          modules=modules,
                          life=data['life'])

        new_story.save()

        return Response(str(new_story.id), status=201)
    except ValidationError as e:
        error.append(str(e))
    except KeyError as e:
        error.append('Missing Key in request body : {}'.format(e))

    return Response(json.dumps({"error": "Sent data is invalid", "message": error}), status=400,
                    headers={"content-type": "application/json"})


@auth
def liste(req, **kwargs):
    queries_story = Story.objects(user_id=kwargs['request_user'].id)
    stories = []
    for s in queries_story:
        stories.append(StoryDTO(s))

    return Response(json.dumps(stories, default=lambda x: x.__dict__), status=200,
                    headers={"content-type": "application/json"})


# Display a story based on the id
def read(req, id):
    try:
        queries_read_story = Story.objects(id=id).first()
        if not queries_read_story:
            return Response(json.dumps({"message": "Resource not found"}), status=404,
                            headers={"content-type": "application/json"})

        return Response(json.dumps(StoryDTO(queries_read_story), default=lambda x: x.__dict__), status=200,
                        headers={"content-type": "application/json"})
    except ValidationError as e:
        return Response(json.dumps({"message": e.message}), status=400,
                        headers={"content-type": "application/json"})
