import sys
from Model.Story import Story, Module, ModuleResponse 
from flask import (current_app as app, json, Response)
from mongoengine import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from Middleware.Auth import auth

@auth
def store(req):
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
          
        new_story = Story(user_id=ObjectId('000000000000000000000000'), # todo: Link with user 
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
       