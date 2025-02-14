from django.http import JsonResponse
from shared.decorators import require_get
from .models import Category
from .serializers.categories_serializers import CategoriesSerializer

@require_get
def category_list(request):
    category_all = Category.objects.all()
    serializer = CategoriesSerializer(category_all, request=request)
    return serializer.json_response()

@require_get
def category_detail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    serializer = CategoriesSerializer(category, request=request)
    return serializer.json_response()
