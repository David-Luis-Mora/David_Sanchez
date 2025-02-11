import json
import logging
import uuid

from django.http import JsonResponse

from games.models import Game
from games.serializers.games_serializers import GamesSerializer
from users.models import Token

# from django.views.decorators.http import require_http_methods
from .models import Order
from .serializers.orders_serializers import OrdersSerializer

logger = logging.getLogger(__name__)


def add_order(request):
    patron = r'Bearer \d{4}-\d{4}-\d{4}-\d{4}'
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    token_key = request.headers.get('Authorization')
    if not token_key or not token_key.startswith('Bearer'):
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    token_key = token_key[7:]

    try:
        uuid.UUID(token_key)
    except ValueError:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    order_new = Order.objects.create(user=token.user)

    serializer = OrdersSerializer(order_new)
    return JsonResponse(
        {
            'id': order_new.pk,
        },
        status=200,
    )


# Preguntar por el modelo Order.price en los test: test_order_detail
def order_detail(request, pk):
    patron = r'Bearer \d{4}-\d{4}-\d{4}-\d{4}'
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        token_key = request.headers.get('Authorization')
        if not token_key or not token_key.startswith('Bearer'):
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        token_key = token_key[7:]

        try:
            uuid.UUID(token_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        serializer = OrdersSerializer(order)
        serialized_data = serializer.serialize_instance(order)

        return JsonResponse(serialized_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)


# Comando para hacer testeo por terminal
# curl -X GET http://127.0.0.1:8000/api/orders/7/games/ -H "Content-Type: application/json" -H "Authorization: Bearer 9500b98c-ffc1-4fd2-931e-89863e5eeb1e"
# El test de test_order_game_list mirar porque da error al comparar la lista de diccionario
def order_game_list(request, pk):
    patron = r'Bearer \d{4}-\d{4}-\d{4}-\d{4}'
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        token_key = request.headers.get('Authorization')
        if not token_key or not token_key.startswith('Bearer'):
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        token_key = token_key[7:]

        try:
            uuid.UUID(token_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        # games = order.games.all()
        list_game = [GamesSerializer(j).serialize() for j in order.games.all()]
        return JsonResponse(list_game, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        logger.error(f'Error creating order: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)


def add_game_to_order(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        game_slug = data.get('game-slug')
        token_key = request.headers.get('Authorization')
        if not token_key or not token_key.startswith('Bearer'):
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

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        try:
            game = Game.objects.get(slug=game_slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        if game.stock <= 0:
            return JsonResponse({'error': 'Game out of stock'})

        order.games.add(game)
        game.stock -= 1
        game.save()

        return JsonResponse({'num-games-in-order': order.games.count()})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'error': str(e)}, status=500)


# def confirm_order(request, pk):
#     # patron = 'Bearer \d{8}[A-Z]'
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#     try:
#         token_key = json.loads(request.headers.get('Authorization'))
#         # token_key = data.get('Authorization')

#         # if token_key := re.search(patron,token_key):
#         #     return JsonResponse({'error': 'Invalid authentication token'},status=400)

#         if not token_key:
#             return JsonResponse({'error': 'Invalid authentication token'}, status=400)

#         try:
#             token = Token.objects.get(key=token_key)
#         except Token.DoesNotExist:
#             return JsonResponse({'error': 'Invalid token'}, status=401)

#         try:
#             order = Order.objects.get(pk=pk)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)

#         if order.user != token.user:
#             return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

#         if order.status != 1:
#             return JsonResponse(
#                 {'error': 'Orders can only be confirmed when initiated'}, status=400
#             )

#         order.status = Order.Status.CONFIRMED
#         order.save()

#         return JsonResponse({'status': order.get_status_display()})

#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid authentication token'}, status=400)


# def cancel_order(request, pk):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#     try:
#         data = json.loads(request.body)
#         token_key = data.get('token')
#         if not token_key:
#             return JsonResponse({'error': 'Invalid authentication token'}, status=400)

#         try:
#             token = Token.objects.get(key=token_key)
#         except Token.DoesNotExist:
#             return JsonResponse({'error': 'Invalid token'}, status=401)

#         try:
#             order = Order.objects.get(pk=pk)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)

#         if order.user != token.user:
#             return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

#         if order.status != 1:
#             return JsonResponse(
#                 {'error': 'Orders can only be cancelled when initiated'}, status=400
#             )

#         for game in order.games.all():
#             game.stock += 1
#             game.save()
#         order.status = Order.Status.CANCELLED
#         order.save()

#         return JsonResponse({'status': order.get_status_display()}, status=200)
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON body'}, status=400)
#     pass


def change_order_status(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        token_key = request.headers.get('Authorization')
        data = json.loads(request.body)
        status = data.get('status')
        # token_key = data.get('Authorization')

        # if token_key := re.search(patron,token_key):
        #     return JsonResponse({'error': 'Invalid authentication token'},status=400)

        if not token_key or not status:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if not token_key.startswith('Bearer'):
            return JsonResponse({'error': 'Invalid authentication token'})

        token_key = token_key[7:]

        try:
            uuid.UUID(token_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        if order.status != 1:
            return JsonResponse(
                {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
            )

        # if status != Order.Status.values:
        #     return JsonResponse({'error': 'Invalid status'})

        order.status = status
        order.save()

        return JsonResponse({'status': order.get_status_display()}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    pass


def pay_order(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        token_key = request.headers.get('Authorization')
        card_number = data.get('card-number')
        exp_date = data.get('exp-date')
        cvc = data.get('cvc')

        if not token_key or not card_number or not exp_date or not cvc:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if not token_key.startswith('Bearer'):
            return JsonResponse({'error': ''}, status=404)

        token_key = token_key[7:]

        try:
            uuid.UUID(token_key)
        except ValueError:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        verf_card = card_number.split('-')
        count = 0
        for j in verf_card:
            if len(j) == 4:
                count += 1
        if len(verf_card) != 4 or count != 4:
            return JsonResponse({'error': 'Invalid card number'}, status=400)

        verf_exp_date = exp_date.split('/')
        if int(verf_exp_date[1][0]) > 3:
            return JsonResponse({'error': 'Invalid expiration date'}, status=400)

        if int(verf_exp_date[1]) < 2024:
            return JsonResponse({'error': 'Card expired'}, status=400)

        if len(cvc) != 3:
            return JsonResponse({'error': 'Invalid CVC'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        if order.status != 2:
            return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)

        order.status = Order.Status.PAID
        order.save()

        return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
