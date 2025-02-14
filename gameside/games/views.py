import json

from django.http import JsonResponse

from shared.decorators import require_get, require_post, validate_json
from users.decorators import auth_required

from .models import Game, Review
from .serializers.games_serializers import GamesSerializer, ReviewsSerializer


@require_get
def game_list(request):
    games_all = Game.objects.all()
    category = request.GET.get('category')
    platform = request.GET.get('platform')
    if category:
        games_all = games_all.filter(category__slug=category)
    if platform:
        games_all = games_all.filter(platforms__slug=platform)
    serializer = GamesSerializer(games_all, request=request)
    return serializer.json_response()


@require_get
def game_detail(request, slug):
    try:
        game = Game.objects.get(slug=slug)
        serializer = GamesSerializer(game, request=request)
        return serializer.json_response()
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)


@require_get
def review_list(request, slug):
    try:
        game = Game.objects.get(slug=slug)
        review = game.reviews.all()
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    serializer = ReviewsSerializer(review, request=request)
    return serializer.json_response()


@require_get
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewsSerializer(review, request=request)
        return serializer.json_response()
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)


@require_post
@validate_json(required_fields=['rating', 'comment'])
@auth_required
def add_review(request, slug):
    try:
        rating = request.json_data['rating']
        comment = request.json_data['comment']
        game = Game.objects.get(slug=slug)
        if not (1 <= rating <= 5):
            return JsonResponse({'error': 'Rating is out of range'}, status=400)
        review = Review.objects.create(
            game=game, author=request.user, rating=rating, comment=comment
        )
        return JsonResponse({'id': review.pk}, status=200)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
