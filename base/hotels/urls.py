from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotels/', views.hotel_search, name='hotel_search'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('review/<int:hotel_id>/', views.add_review, name='add_review'),
]
