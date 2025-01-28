# Create your views here.

from .models import Category
from .serializers.categories_serializers import CategoriesSerializer


def category_list(request):
    category_all = Category.objects.all()
    serializer = CategoriesSerializer(category_all)

    return serializer.serialize_instance()


def category_detail(request):
    pass
