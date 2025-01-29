from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

# from django.views.decorators.http import require_http_methods
from .models import Game, Review
from .serializers.games_serializers import GamesSerializer, ReviewsSerializer


def game_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        games_all = Game.objects.all()
        serializer = GamesSerializer(games_all, request=request)
        return serializer.json_response()


def game_detail(request,slug):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        game = Game.objects.get(slug=slug)
        serializer = GamesSerializer(game, request=request)
        return serializer.json_response()


def review_list(request, slug):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        game = Game.objects.get(slug=slug)
        review = game.reviews.all()
        # game = Review.objects.get(game=slug)
        game = Review.objects.all()

        serializer = ReviewsSerializer(review, request=request)
        return serializer.json_response()
    


def review_detail(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        review = Review.objects.get(pk=pk)
        serializer = ReviewsSerializer(review, request=request)
        return serializer.json_response()


# def add_review(request, slug):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

#     else:
#         review = Review.objects.get()
#         serializer = ReviewsSerializer(review, request=request)
#         return serializer.json_response()
