from django.http import JsonResponse
from functools import wraps
import json
def require_get(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view_func(request, *args, **kwargs)
    return wrapper

def require_post(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view_func(request, *args, **kwargs)
    return wrapper

def validate_json(required_fields=None):
    def wrapper(view_func):
        def inner(request, *args, **kwargs):
            data = {}
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) if request.body else {}
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON body'}, status=400)
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return JsonResponse({'error': f'Missing required fields'}, status=400)
            request.json_data = data
            return view_func(request, *args, **kwargs)
        return inner
    return wrapper


