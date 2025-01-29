from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

# from django.views.decorators.http import require_http_methods
from .models import Token
from .serializers.users_serializers import TokensSerializer

def auth(request, username, password):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        token_all = Token.objects.get(username=username, password=password )
        serializer = TokensSerializer(token_all, request=request)
        return serializer.json_response()
