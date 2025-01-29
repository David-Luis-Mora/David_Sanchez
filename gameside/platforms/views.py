# Create your views here.

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

# from django.views.decorators.http import require_http_methods
from .models import Platform
from .serializers.platforms_serializers import PlatformSerializer


# @require_http_methods(['GET'])
def platform_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        platforms_all = Platform.objects.all()
        serializer = PlatformSerializer(platforms_all, request=request)
        return serializer.json_response()

def platform_detail(request, slug):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        try:
            platform = get_object_or_404(Platform, slug=slug)
            serializer = PlatformSerializer(platform, request=request)
            return serializer.json_response()

        except Http404:
            return JsonResponse({'error': 'Platform not found'}, status=404)
        
