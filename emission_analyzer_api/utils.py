import json
from django.http import JsonResponse
from .responses import *
from .constants import ErrorCode, ErrorType

def parse_model_output(s):
    try:
        parsed_output = json.loads(s)

        if "output" in parsed_output:
            parsed_output["output"] = json.loads(parsed_output["output"])
        return parsed_output
    
    except json.JSONDecodeError as e:
        raise Error(e, ErrorCode.DECODE_ERROR, ErrorType.PREDICTION_MODEL, 500)
    
def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError as e:
        raise Error(e, ErrorCode.DECODE_ERROR, ErrorType.CLIENT, 400)
    
def validate_keys(data, required_keys, error_message=None):
    missing = [key for key in required_keys if key not in data]
    extra = [key for key in data if key not in required_keys]

    if missing:
        message = error_message or f"Missing required field(s): {', '.join(missing)}"
        raise Error(message, ErrorCode.MISSING_FIELD, ErrorType.CLIENT, 400)

    if extra:
        message = f"Invalid field(s) provided: {', '.join(extra)}"
        raise Error(message, ErrorCode.VALIDATION_ERROR, ErrorType.CLIENT, 400)
    
def error_response(message, code, type, status):
    return JsonResponse({
        "error": message,
        "error_code": code,
        "error_type": type
    }, status=status)