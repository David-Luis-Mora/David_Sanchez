# Create your views here.
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
import json

from users.models import Token
# from django.views.decorators.http import require_http_methods
from .models import Order
from games.models import Game
from .serializers.orders_serializers import OrdersSerializer
from games.serializers.games_serializers import GamesSerializer

import logging

logger = logging.getLogger(__name__)





def add_order(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        token_key = data.get('token')
        if not token_key:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        order_new = Order.objects.create(user=token.user)

        serializer = OrdersSerializer(order_new)
        return JsonResponse({
            'id': order_new.pk,
            'order': serializer.serialize_instance(order_new)
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")  # Log the error
        return JsonResponse({'error': str(e)}, status=500)


#Preguntar por el modelo Order.price en los test: test_order_detail
def order_detail(request,pk):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        token_key = data.get('token')
        if not token_key:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

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
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# Comando para hacer testeo por terminal
# curl -X POST http://127.0.0.1:8000/api/orders/26/games/ -H "Content-Type: application/json" -d '{"token": "a11ec6d0-e613-4626-afe6-fa42e150194d"}'
#El test de test_order_game_list mirar porque da error al comparar la lista de diccionario
def order_game_list(request,pk):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)

        token_key = data.get('token')
        if not token_key:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        games = order.games.all()
        serializer = GamesSerializer(games)
        serialized_data = serializer.serialize_queryset(games)
        print(serialized_data)
        return JsonResponse({'games': serialized_data}, status=200)
       

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


def add_game_to_order(request,pk,slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        token_key = data.get('token')
        if  not token_key:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status = 404)
        
        try:
            game = Game.objects.get(slug=slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status = 404)

        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        
        
        if game.stock <= 0:
            return JsonResponse({'error': 'Game out of stock'})
        
        order.games.add(game)
        game.stock -= 1
        game.save()

        return JsonResponse({'num-games-in-order': order.games.count()},status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




def confirm_order(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        token_key = data.get('token')

        if not token_key:
            return JsonResponse({'error': 'Missing required fields'},status=400)

        try:
            token = Token.objects.get(key = token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'},status=401)
        

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        
        if order.user != token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        
        if order.status != 1:
            return JsonResponse({'error': 'Orders can only be confirmed when initiated'}, status=400)

        order.status = Order.Status.CONFIRMED
        order.save()

        return JsonResponse({'status': order.get_status_display()})
    
    except json.JSONDecodeError:
        return JsonResponse({'error':'Invalid JSON body'}, status=400)


def cancel_order(request):
    pass


def pay_order(request):
    pass
