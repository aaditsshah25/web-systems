from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('slots/', views.slots_view, name='slots'),
    path('book/', views.book_slot_view, name='book'),
    path('my_bookings/', views.my_bookings_view, name='my_bookings'),
]