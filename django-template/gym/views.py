import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.utils import timezone

from .models import Slot, Booking

import os
import socket
import threading
import datetime
import django

@csrf_exempt
def register_view(request):
    """API endpoint for user registration."""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'success': True, 'user_id': user.id})
        except IntegrityError:
            return JsonResponse({'error': 'Username already taken'}, status=400)
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def login_view(request):
    """API endpoint for user login."""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'username': user.username
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def slots_view(request):
    """API endpoint for listing available slots."""
    if request.method == 'GET':
        today = timezone.now().date()
        slots = Slot.objects.filter(date__gte=today)
        
        slots_data = [
            {
                'id': slot.id,
                'date': slot.date.strftime('%Y-%m-%d'),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
                'available': slot.available,
                'capacity': slot.capacity
            }
            for slot in slots
        ]
        
        return JsonResponse({'slots': slots_data})
    
    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

@csrf_exempt
def book_slot_view(request):
    """API endpoint for booking a slot."""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        data = json.loads(request.body)
        slot_id = data.get('slot_id')
        
        if not slot_id:
            return JsonResponse({'error': 'Slot ID is required'}, status=400)
        
        try:
            with transaction.atomic():
                slot = Slot.objects.select_for_update().get(id=slot_id)
                
                if slot.available <= 0:
                    return JsonResponse({'error': 'No available space in this slot'}, status=400)
                
                # Check if user already has a booking for this slot
                if Booking.objects.filter(user=request.user, slot=slot).exists():
                    return JsonResponse({'error': 'You already have a booking for this slot'}, status=400)
                
                # Create booking and update slot availability
                booking = Booking.objects.create(user=request.user, slot=slot)
                slot.available -= 1
                slot.save()
                
                return JsonResponse({
                    'success': True,
                    'booking_id': booking.id,
                    'slot_id': slot.id,
                    'date': slot.date.strftime('%Y-%m-%d'),
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                })
                
        except Slot.DoesNotExist:
            return JsonResponse({'error': 'Slot not found'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Booking failed'}, status=400)
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def my_bookings_view(request):
    """API endpoint for viewing user's bookings."""
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        bookings = Booking.objects.filter(user=request.user).select_related('slot')
        
        bookings_data = [
            {
                'id': booking.id,
                'date': booking.slot.date.strftime('%Y-%m-%d'),
                'start_time': booking.slot.start_time.strftime('%H:%M'),
                'end_time': booking.slot.end_time.strftime('%H:%M'),
                'booked_at': booking.booked_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for booking in bookings
        ]
        
        return JsonResponse({'bookings': bookings_data})
    
    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

# ...existing code...

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def home_view(request):
    """Render the home page."""
    return render(request, 'gym/home.html')

def register_page_view(request):
    """Render the registration page."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email', '')
        
        if not username or not password1:
            return render(request, 'gym/register.html', {'error': 'Username and password are required'})
        
        if password1 != password2:
            return render(request, 'gym/register.html', {'error': 'Passwords do not match'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            return redirect('login_page')
        except IntegrityError:
            return render(request, 'gym/register.html', {'error': 'Username already taken'})
    
    return render(request, 'gym/register.html')

def login_page_view(request):
    """Render the login page."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'gym/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'gym/login.html')

def logout_view(request):
    """Log the user out."""
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    """Render the user dashboard."""
    return render(request, 'gym/dashboard.html')

@login_required
def view_slots_view(request):
    """Render the available slots page."""
    today = timezone.now().date()
    slots = Slot.objects.filter(date__gte=today)
    return render(request, 'gym/slots.html', {'slots': slots})

@login_required
def view_bookings_view(request):
    """Render the user's bookings page."""
    bookings = Booking.objects.filter(user=request.user).select_related('slot')
    return render(request, 'gym/bookings.html', {'bookings': bookings})

@login_required
def book_slot_web_view(request):
    """Handle booking a slot from the web interface."""
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        
        if not slot_id:
            return redirect('view_slots')
        
        try:
            with transaction.atomic():
                slot = Slot.objects.select_for_update().get(id=slot_id)
                
                if slot.available <= 0:
                    return render(request, 'gym/slots.html', {
                        'slots': Slot.objects.filter(date__gte=timezone.now().date()),
                        'message': 'No available space in this slot',
                        'success': False
                    })
                
                # Check if user already has a booking for this slot
                if Booking.objects.filter(user=request.user, slot=slot).exists():
                    return render(request, 'gym/slots.html', {
                        'slots': Slot.objects.filter(date__gte=timezone.now().date()),
                        'message': 'You already have a booking for this slot',
                        'success': False
                    })
                
                # Create booking and update slot availability
                booking = Booking.objects.create(user=request.user, slot=slot)
                slot.available -= 1
                slot.save()
                
                return render(request, 'gym/slots.html', {
                    'slots': Slot.objects.filter(date__gte=timezone.now().date()),
                    'message': 'Slot booked successfully!',
                    'success': True
                })
                
        except Slot.DoesNotExist:
            return render(request, 'gym/slots.html', {
                'slots': Slot.objects.filter(date__gte=timezone.now().date()),
                'message': 'Slot not found',
                'success': False
            })
    
    return redirect('view_slots')