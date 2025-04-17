from django.http import HttpResponse, JsonResponse
from .models import Engine
from django.views.decorators.csrf import csrf_exempt
from .services import *
from .utils import *
from .constants import *
from .helpers import *

def index(request):
    return HttpResponse("This is the Emission Analyzer API index.")

@csrf_exempt
def getEngineTypes(request):
    if request.method != HTTP_METHOD.GET:
        return error_response(
            "Invalid request method",
            ErrorCode.INVALID_METHOD,
            ErrorType.CLIENT,
            400
        )
    
    types = get_engines_types()
    
    return Success({"engine_types": types}, "Retrieved engine types").to_json()

@csrf_exempt
def getUser(request, user_id):
    if request.method != HTTP_METHOD.GET:
        return error_response(
            "Invalid request method",
            ErrorCode.INVALID_METHOD,
            ErrorType.CLIENT,
            400
        )
    
    try:
        user = get_user(user_id)

        response = Success({ "user_id": user.user_id }, "User retrieved")
        return response.to_json()

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status)
        

@csrf_exempt
def getEngines(request, user_id):
    if request.method != HTTP_METHOD.GET:
        return error_response(
            "Invalid request method",
            ErrorCode.INVALID_METHOD,
            ErrorType.CLIENT,
            400
        )
    try:
        user = get_user(user_id)
        engines = get_engines(user)

        response = Success({ "user_id": user_id, "engines": engines }, "Engines retrieved")
        return response.to_json()

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status)
    
@csrf_exempt
def addEngine(request):
    try:
        if request.method != HTTP_METHOD.POST:
            raise Error("Invalid request method", ErrorCode.INVALID_METHOD, ErrorType.CLIENT, 400)
        
        data = parse_request_body(request)
        user, engine_type = request_validation(data)

        if Engine.objects.filter(user=user, engine_identification=data[ENGINE][ENGINE_ID]).exists():
            raise Error("Engine already associated with user", ErrorCode.ALREADY_EXISTS, ErrorType.CLIENT, status=400)
        
        engine = add_engine(data, user, engine_type)

        response = PostSuccess(engine.to_json(), "Engine successfully added")
        return response.to_json()
    
    except Error as e:
        return error_response(str(e), e.code, e.type, e.status)

@csrf_exempt
def editEngine(request):
    try:
        if request.method != HTTP_METHOD.PUT:
            raise Error("Invalid request method", ErrorCode.INVALID_METHOD, ErrorType.CLIENT, 400)
        
        data = parse_request_body(request)
        user, engine_type = request_validation(data)

        engine = Engine.objects.get(user=user, engine_identification=data[ENGINE][ENGINE_ID])
        engine = edit_engine(engine, engine_type, data[ENGINE])

        response = Success(engine.to_json(), "Engine updated successfully")
        return response.to_json()

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status)
    
@csrf_exempt
def createUser(request):
    try:
        if request.method != HTTP_METHOD.POST:
            raise Error("Invalid request method", ErrorCode.INVALID_METHOD, ErrorType.CLIENT, 400)
        
        data = parse_request_body(request)
        validate_keys(data, [USER_ID])
        user, created = create_user(data[USER_ID])

        if created:
            return PostSuccess({ "user_id": user.user_id }, "User created").to_json()
        else:
            return Success({ "user_id": user.user_id }, "User already exists").to_json()

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status)
    
@csrf_exempt
def predictEmissions(request):
    if request.method != HTTP_METHOD.POST:
        return JsonResponse({ "error": "invalid request method" }, status=405)
    
    try:
        data = parse_request_body(request)
        validate_keys(data, [BP_RATIO, PRESSURE_RATIO, RATED_THRUST])
        
        result = perform_prediction(
            data[BP_RATIO], data[PRESSURE_RATIO], data[RATED_THRUST]
        )
        
        return JsonResponse({ "predictions": result }, status=200)

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status, e.status)
