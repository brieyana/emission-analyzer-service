from django.http import HttpResponse, JsonResponse
import json
from .models import User, Engine, EngineType
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("This is the Emission Analyzer API index.")

@csrf_exempt
def getUser(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(user_id=user_id)

            if user:
                return JsonResponse({ "user_id": user_id }, status=200)
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
    return JsonResponse({"error": "invalid request method"}, status=405)

@csrf_exempt
def addUser(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body) #loads json data into a dictionary
            user_id = data.get("user_id") #extracts 'user_id' from json body

            if not user_id:
                return JsonResponse({ "error": "missing user_id" }, status=400)
            
            user, created = User.objects.get_or_create(user_id=user_id) #creates a new user if it doesn't exist, otherwise returns the existing user

            if created:
                return JsonResponse({ "message": "user created successfully", "user_id": user.user_id }, status=201) #201 creates data
            else:
                return JsonResponse({ "message": "user already exists", "user_id": user.user_id }, status=200) #200 returns existing data
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid JSON format"}, status=400)

    return JsonResponse({"error": "invalid request method"}, status=405)

@csrf_exempt
def addEngine(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Load JSON from request body

            user_id = data.get("user_id")
            engine_data = data.get("engine")

            # error case 1
            if not user_id:
                return JsonResponse({ "error": "missing user id" }, status=400)
            # error case 2
            if not engine_data:
                return JsonResponse({ "error": "missing engine data" }, status=400)

            engine_id = engine_data.get("engine_identification")
            engine_type_name = engine_data.get("engine_type")
            rated_thrust = engine_data.get("rated_thrust")
            bp_ratio = engine_data.get("bp_ratio")
            pressure_ratio = engine_data.get("pressure_ratio")

            # error case 3
            if not all([engine_id, engine_type_name, rated_thrust, bp_ratio, pressure_ratio]):
                return JsonResponse({ "error": "missing 1+ engine fields" }, status=400)

            # error case 4
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return JsonResponse({ "error": "user does not exist" }, status=404)

            # error case 5
            try:
                engine_type = EngineType.objects.get(type=engine_type_name)
            except EngineType.DoesNotExist:
                return JsonResponse({ "error": "engine type not found" }, status=404)

            # error case 8
            if Engine.objects.filter(engine_identification=engine_id).exists():
                return JsonResponse({ "error": "engine already exists" }, status=400)
            else:
                engine = Engine.objects.create(
                    user=user,
                    engine_identification=engine_id,
                    engine_type=engine_type,  # CHANGE: Pass engine_type object, not type name
                    rated_thrust=rated_thrust,
                    bp_ratio=bp_ratio,
                    pressure_ratio=pressure_ratio
                )

            return JsonResponse({
                "message": "engine successfully created",
                "engine": {
                    "user": user.user_id,
                    "engine_identification": engine.engine_identification,
                    "engine_type_id": engine_type.id,
                    "engine_type": engine_type.type,
                    "rated_thrust": float(engine.rated_thrust),  # Convert Decimal to float
                    "bp_ratio": float(engine.bp_ratio),  # Convert Decimal to float
                    "pressure_ratio": float(engine.pressure_ratio)  # Convert Decimal to float
                }
            }, status=201)

        # error case 6
        except json.JSONDecodeError:
            return JsonResponse({ "error": "invalid JSON format" }, status=400)

    # error case 7
    return JsonResponse({ "error": "invalid request method" }, status=405)