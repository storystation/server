from flask import Blueprint, request
from Controller import StoryController

bp = Blueprint('story', __name__, url_prefix='/story')

@bp.route('/', methods=['POST'])
def create_story(): return StoryController.store(req=request)
