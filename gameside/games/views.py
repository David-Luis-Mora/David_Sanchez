from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
import json

from users.models import Token
# from django.views.decorators.http import require_http_methods
from .models import Game, Review
from .serializers.games_serializers import GamesSerializer, ReviewsSerializer
import uuid
from users.decorators import auth_required
from shared.decorators import require_get, require_post, validate_json

@require_get
def game_list(request):
    games_all = Game.objects.all() 
    category = request.GET.get('category')
    platform = request.GET.get('platform')
    if category:
        games_all = games_all.filter(category__slug=category)
    if platform:
        games_all = games_all.filter(platforms__slug =platform)
    serializer = GamesSerializer(games_all, request=request)
    return serializer.json_response()

@require_get
def game_detail(request,slug):
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
        return JsonResponse({'error': 'Review not found'},status=404)


@require_post
@validate_json(required_fields=['rating', 'comment'])  # Verificación de campos requeridos en el decorador
@auth_required
def add_review(request,slug):

    try:
        data = json.loads(request.body)
        token_key = request.headers.get('Authorization')
        rating = data.get('rating')
        comment = data.get('comment')


        if not token_key or not rating or not comment :
            return JsonResponse({'error': 'Missing required fields'}, status=400)


        # token_key = token_key[7:]

        # try:
        #     uuid.UUID(token_key)
        # except ValueError:
        #     return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        


        # try:
        #     token = Token.objects.get(key=token_key)
        # except Token.DoesNotExist:
        #     return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        game = Game.objects.get(slug=slug)

        if not (1 <= rating <= 5):
            return JsonResponse({'error': 'Rating is out of range'}, status=400)

        review = Review.objects.create(
            game=game,
            author=request.user,
            rating=rating,
            comment=comment
        )
        return JsonResponse({'id': review.pk}, status=200)

    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)