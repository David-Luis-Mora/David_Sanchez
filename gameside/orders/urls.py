from django.urls import path

from . import views

app_name = 'orders'


urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
    path('<int:pk>/games/', views.order_game_list, name='order-game-list'),
    path('<int:pk>/games/add/', views.add_game_to_order, name='add-game-to-order'),
    path('<int:pk>/status/', views.change_order_status, name='change-order-status'),
    # path('<int:pk>/confirm/', views.confirm_order, name='confirm-order'),
    # path('<int:pk>/cancel/', views.cancel_order, name='cancel-order'),
    path('<int:pk>/pay/', views.pay_order, name='pay-order'),
]
