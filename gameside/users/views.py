from django.http import JsonResponse
import json
from django.contrib.auth import authenticate
from shared.decorators import require_get, require_post, validate_json
from .models import Token

@require_post
@validate_json(required_fields=['username','password'])
def auth(request):
    username =request.json_data['username']
    password =request.json_data['password']
    user = authenticate(request,username=username, password=password)
    if user:
        request.user = user
        token = Token.objects.get(user=user)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'token': token.key}, status=200)
