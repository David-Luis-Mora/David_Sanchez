from django.http import JsonResponse
from .models import Platform
from .serializers.platforms_serializers import PlatformSerializer
from shared.decorators import require_get, require_post

@require_get
def platform_list(request):
    platforms_all = Platform.objects.all()
    serializer = PlatformSerializer(platforms_all, request=request)
    return serializer.json_response()
    
@require_get
def platform_detail(request, slug):
    try:
        platform = Platform.objects.get(slug=slug)
    except Platform.DoesNotExist:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()
        
