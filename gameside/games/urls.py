from django.urls import path

from . import views

app_name = 'games'


urlpattens = [
    path('', views.game_list, name='game-list'),
    path('<str:name>/', views.game_detail, name='game-detail'),
    path('<str:name>/reviews/', views.review_list, name='review-list'),
    path('reviews/<int:pk>/', views.review_detail, name='review-detail'),
    path('<str:name/reviews/>add/', views.add_review, name='add_review'),
]
