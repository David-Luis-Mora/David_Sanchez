import json
import uuid
from django.http import JsonResponse
from games.models import Game
from games.serializers.games_serializers import GamesSerializer
from users.models import Token
from .models import Order
from .serializers.orders_serializers import OrdersSerializer
from users.decorators import auth_required
from shared.decorators import require_get, require_post, validate_json
from  .validator import validate_card_data

@require_post
@auth_required
def add_order(request):
    order_new = Order.objects.create(user=request.user)
    serializer = OrdersSerializer(order_new)
    return JsonResponse({'id': order_new.pk,},status=200)

@require_get
@auth_required
@validate_json(required_fields=[])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    if order.user != request.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    serializer = OrdersSerializer(order)
    serialized_data = serializer.serialize_instance(order)
    return JsonResponse(serialized_data, status=200)

@require_get
@auth_required
@validate_json(required_fields=[])
def order_game_list(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    if order.user != request.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    list_game = [GamesSerializer(j).serialize() for j in order.games.all()]
    return JsonResponse(list_game, safe=False)

@require_post
@validate_json(required_fields=['game-slug'])
@auth_required
def add_game_to_order(request, pk):
    game_slug = request.json_data['game-slug']
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    if order.user != request.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    if game.stock <= 0:
        return JsonResponse({'error': 'Game out of stock'})
    order.games.add(game)
    game.stock -= 1
    game.save()
    return JsonResponse({'num-games-in-order': order.games.count()})

@require_post
@validate_json(required_fields=['status'])
@auth_required
def change_order_status(request, pk):
    status = request.json_data['status']
    VALID_STATUSES = {Order.Status.CANCELLED, Order.Status.CONFIRMED}
    if status not in VALID_STATUSES:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    if order.user != request.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    if order.status != 1:
        return JsonResponse(
            {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
        )
    order.status = status
    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)

@require_post
@validate_json(required_fields=['card-number','exp-date','cvc'])
@auth_required
def pay_order(request, pk):
    card_number = request.json_data['card-number']
    exp_date = request.json_data['exp-date']
    cvc = request.json_data['cvc']
    card_validation_error = validate_card_data(card_number, exp_date, cvc)
    if card_validation_error:
        return JsonResponse(card_validation_error, status=400)
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    if order.user != request.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    if order.status != 2:
        return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
    order.status = Order.Status.PAID
    order.save()
    return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)
