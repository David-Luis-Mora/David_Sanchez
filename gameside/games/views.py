from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
import json

from users.models import Token
# from django.views.decorators.http import require_http_methods
from .models import Game, Review
from .serializers.games_serializers import GamesSerializer, ReviewsSerializer
import uuid


def game_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        games_all = Game.objects.all() 
        category = request.GET.get('category')
        platform = request.GET.get('platform')
        if category:
            games_all = games_all.filter(category__slug=category)
        if platform:
            games_all = games_all.filter(platforms__slug =platform)
        serializer = GamesSerializer(games_all, request=request)
        return serializer.json_response()
    except Http404:
       return JsonResponse({'error': 'Category not found'}, status=404)

        


def game_detail(request,slug):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        try:
            game = get_object_or_404(Game,slug=slug)
            serializer = GamesSerializer(game, request=request)
            return serializer.json_response()
        except Http404:
            return JsonResponse({'error': 'Game not found'}, status=404)
       


def review_list(request, slug):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        try:
            game = Game.objects.get(slug=slug)
            review = game.reviews.all()
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

        serializer = ReviewsSerializer(review, request=request)
        return serializer.json_response()
    


def review_detail(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewsSerializer(review, request=request)
            return serializer.json_response()
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'},status=404)



def add_review(request,slug):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        token_key = request.headers.get('Authorization')
        rating = data.get('rating')
        comment = data.get('comment')


        if not token_key or not rating or not comment :
            return JsonResponse({'error': 'Missing required fields'}, status=400)


        token_key = token_key[7:]

        try:
            uuid.UUID(token_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        


        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        game = Game.objects.get(slug=slug)

        if not (1 <= rating <= 5):
            return JsonResponse({'error': 'Rating is out of range'}, status=400)

        review = Review.objects.create(
            game=game,
            author=token.user,
            rating=rating,
            comment=comment
        )
        return JsonResponse({'id': review.pk}, status=200)

    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)