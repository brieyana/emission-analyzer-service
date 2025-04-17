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
        
        # Validate required fields in request payload
        validate_keys(data, [USER_ID, ENGINE_ID])
        user_id = data[USER_ID]
        engine_id = data[ENGINE_ID]
        
        # Validate user exists
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({ "error": "User not found" }, status=404)
        
        # Validate engine exists for this user
        try:
            engine = Engine.objects.get(user=user, engine_identification=engine_id)
        except Engine.DoesNotExist:
            return JsonResponse({ "error": "Engine not found for this user" }, status=404)
        
        # Use engine parameters from database to perform prediction
        result = perform_prediction(
            float(engine.bp_ratio), 
            float(engine.pressure_ratio), 
            float(engine.rated_thrust)
        )
        
        # Store prediction results in the database
        for emission_type_name, prediction_data in result.items():
            # Get or create the EmissionType
            emission_type, _ = EmissionType.objects.get_or_create(name=emission_type_name)
            
            # Get or create the EmissionClass
            emission_class, _ = EmissionClass.objects.get_or_create(label=prediction_data["Class"])
            
            # Create the Prediction record
            Prediction.objects.create(
                engine=engine,
                emission_type=emission_type,
                emission_class=emission_class,
                confidence_levels=prediction_data["Confidence"]
            )
        
        return JsonResponse({ "predictions": result }, status=200)

    except Error as e:
        return error_response(str(e), e.code, e.type, e.status, e.status)
