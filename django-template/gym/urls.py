from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('slots/', views.slots_view, name='slots'),
    path('book/', views.book_slot_view, name='book'),
    path('my_bookings/', views.my_bookings_view, name='my_bookings'),
    path('api/calendar-slots/', views.calendar_slots_api, name='calendar_slots_api'),
    
    # Web interface
    path('', views.home_view, name='home'),
    path('register-page/', views.register_page_view, name='register_page'),
    path('login-page/', views.login_page_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('view-slots/', views.view_slots_view, name='view_slots'),
    path('view-bookings/', views.view_bookings_view, name='view_bookings'),
    path('book-slot-web/', views.book_slot_web_view, name='book_slot_web'),
    path('calendar/', views.calendar_view, name='calendar_view'),

    # Special class & trainer URLs
    path('special-classes/', views.view_special_classes_view, name='view_special_classes'),
    path('book-special-class/', views.book_special_class_view, name='book_special_class'),
    path('trainer-bookings/', views.view_trainer_bookings_view, name='view_trainer_bookings'),
    path('trainers/', views.trainers_view, name='trainers'),
    path('trainers/<int:trainer_id>/', views.trainer_detail_view, name='trainer_detail'),
]