from django.http import JsonResponse

class Error(Exception):
    def __init__(self, message, code, type, status):
        super().__init__(message)
        self.code = code
        self.type = type
        self.status = status

class Success:
    def __init__(self, data, message, status=200):
        self.data = data
        self.message = message
        self.status = status

    def to_json(self):
        return JsonResponse({
            "message": self.message,
            "data": self.data
        }, status=self.status)
    
class PostSuccess(Success):
    def __init__(self, data, message, status=201):
        self.data = data
        self.message = message
        self.status = status
