from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth import authenticate

from .models import Token
from .serializers.users_serializers import TokensSerializer

def auth(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username or  not password:
            return JsonResponse({'error': 'Missing required fields'},status=400)

        user = authenticate(request,username=username, password=password)
            

        if user:
            request.user = user
            token = Token.objects.get(user=user)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        return JsonResponse({'token': token.key}, status=200)   

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
