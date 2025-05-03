from django.http import HttpResponse, JsonResponse
from .models import Engine
from .services import *
from .utils import *
from .constants import *
from .helpers import *
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})


def deleteEngine(request, user_id, engine_id):
    if request.method != HTTP_METHOD.DELETE:
        return error_response(
            "Invalid request method",
            ErrorCode.INVALID_METHOD,
            ErrorType.CLIENT,
            400
        )
    
    try:
        user = get_user(user_id)
        delete_engine(user, engine_id)

        return HttpResponse(status=204)
    except Error as e:
        return error_response(str(e), e.code, e.type, e.status)

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

def predictEmissions(request):
    if request.method != HTTP_METHOD.POST:
        return JsonResponse({ "error": "invalid request method" }, status=405)
    
    try:
        data = parse_request_body(request)
        
        # Validate required fields in request payload
        validate_keys(data, [USER_ID, ENGINE_ID])
        user_id = data[USER_ID]
        engine_id = data[ENGINE_ID]

        user = get_user(user_id)
        engine = get_engine(user, engine_id)
        
        # Use engine parameters from database to perform prediction
        result = perform_prediction(
            float(engine.bp_ratio), 
            float(engine.pressure_ratio), 
            float(engine.rated_thrust)
        )
        
        return JsonResponse({ "predictions": result }, status=200)

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status, e.status)
