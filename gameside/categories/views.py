# Create your views here.

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

# from django.views.decorators.http import require_http_methods
from .models import Category
from .serializers.categories_serializers import CategoriesSerializer


# @require_http_methods(['GET'])
def category_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        category_all = Category.objects.all()
        serializer = CategoriesSerializer(category_all, request=request)
        return serializer.json_response()


def category_detail(request, slug):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        try:
            category = get_object_or_404(Category, slug=slug)
        except Http404:
            return JsonResponse({'error': 'Category not found'}, status=404)
        # category_all = Category.objects.get(slug=slug)
        # category = get_object_or_404(Category, slug=slug)
        serializer = CategoriesSerializer(category, request=request)
        return serializer.json_response()
