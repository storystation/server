import sys
from DTO.StoryDTO import StoryDTO
from Model.Story import Story, Module, ModuleResponse 
from flask import (current_app as app, json, Response)
from mongoengine import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from Middleware.Auth import auth

@auth
def store(req, **kwargs):
    data = req.get_json()
    error = []
    
    try:
        modules = []
        for m in data['modules']:
            rs = ModuleResponse(success=m['response']['success'], fail=m['response']['fail'])
            mo = Module(
                _id=ObjectId(m['_id']),
                name=m['name'], 
                description=m['description'],
                response=rs,
                components=m['components'],
                _type=m['type'],
                time_max=m['time_max'],
                position=m['position'],
                win_condition=m['win_condition'])
            modules.append(mo)
          
        new_story = Story(user_id=ObjectId(str(kwargs['request_user'].id)), # todo: Link with user 
            character_name=data['character_name'], 
            stage=data['stage'],
            modules=modules,
            components=data['components'],
            companion_name=data['companion_name'],
            life=data['life'])

        new_story.save()
    except (ValidationError) as e:
        error.append(str(e))
    except(KeyError) as e:
        error.append('Missing Key in request body : {}'.format(e) )   

    if error.__len__() > 0:
        return Response(json.dumps({"error": "Sent data is invalid", "message": error}), status=400,
                        headers={"content-type": "application/json"})               

    return Response(str(new_story.id), status=201)
       

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