from .models import *
from django.http import Http404
from .responses import Error
from .constants import *
from .utils import *
from .services import get_user, get_engine_type
import numbers
    
def validate_types(data: dict, expected_types: dict):
    for key, expected_type in expected_types.items():
        if not isinstance(data[key], expected_type):
            raise Error(
                f"Invalid type for key '{key}': expected {expected_type.__name__}, got {type(data[key]).__name__}",
                ErrorCode.VALIDATION_ERROR,
                ErrorType.CLIENT,
                400
            )

def request_validation(data):
    validate_keys(data, [USER_ID, ENGINE])
    user = get_user(data[USER_ID])
    validate_keys(data[ENGINE], [ENGINE_ID, ENGINE_TYPE, BP_RATIO, PRESSURE_RATIO, RATED_THRUST])
    validate_types(data[ENGINE], {
        ENGINE_ID: str,
        ENGINE_TYPE: str,
        BP_RATIO: numbers.Number,
        PRESSURE_RATIO: numbers.Number,
        RATED_THRUST: numbers.Number
    })
    
    engine_type = get_engine_type(data[ENGINE][ENGINE_TYPE])
    return user, engine_type