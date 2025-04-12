from .models import *
from django.http import Http404

def validate_user(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found")

def validate_engine_type(engine_type):
    try:
        return EngineType.objects.get(type=engine_type)
    except EngineType.DoesNotExist:
        raise Http404("Engine Type not found")