from django.http import HttpResponse, JsonResponse
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("This is the Emission Analyzer API index.")

@csrf_exempt
def addUser(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")

            if not user_id:
                return JsonResponse({ "error": "missing user_id" }, status=400)
            
            user, created = User.objects.get_or_create(user_id=user_id)

            if created:
                return JsonResponse({ "message": "user created successfully", "user_id": user.user_id }, status=201)
            else:
                return JsonResponse({ "message": "user already exists", "user_id": user.user_id }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid JSON format"}, status=400)

    return JsonResponse({"error": "invalid request method"}, status=405)   
