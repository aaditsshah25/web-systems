import requests
import json
import argparse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError

class GymBookingClient:
    """Client for interacting with the Gym Booking API."""
    
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url
    
    def register(self, username, password, email=None):
        """Register a new user."""
        url = f"{self.base_url}/register/"
        data = {
            'username': username,
            'password': password,
        }
        if email:
            data['email'] = email
            
        response = self.session.post(url, json=data)
        return response.json()
    
    def login(self, username, password):
        """Login a user."""
        url = f"{self.base_url}/login/"
        data = {
            'username': username,
            'password': password,
        }
        
        response = self.session.post(url, json=data)
        return response.json()
    
    def get_slots(self):
        """Get available slots."""
        url = f"{self.base_url}/slots/"
        response = self.session.get(url)
        return response.json()
    
    def book_slot(self, slot_id):
        """Book a slot."""
        url = f"{self.base_url}/book/"
        data = {
            'slot_id': slot_id,
        }
        
        response = self.session.post(url, json=data)
        return response.json()
    
    def get_my_bookings(self):
        """Get user's bookings."""
        url = f"{self.base_url}/my_bookings/"
        response = self.session.get(url)
        return response.json()
    
    def pretty_print(self, data):
        """Pretty print JSON data."""
        print(json.dumps(data, indent=4))

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

def main():
    """Command-line interface for the client."""
    parser = argparse.ArgumentParser(description='Gym Booking System Client')
    parser.add_argument('--base-url', default='http://127.0.0.1:8000/api',
                      help='Base URL for the API (default: http://127.0.0.1:8000/api)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Register command
    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('username', help='Username')
    register_parser.add_argument('password', help='Password')
    register_parser.add_argument('--email', help='Email address')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login a user')
    login_parser.add_argument('username', help='Username')
    login_parser.add_argument('password', help='Password')
    
    # Slots command
    subparsers.add_parser('slots', help='List available slots')
    
    # Book command
    book_parser = subparsers.add_parser('book', help='Book a slot')
    book_parser.add_argument('slot_id', type=int, help='Slot ID to book')
    
    # My bookings command
    subparsers.add_parser('my-bookings', help='List my bookings')
    
    args = parser.parse_args()
    client = GymBookingClient(base_url=args.base_url)
    
    if args.command == 'register':
        result = client.register(args.username, args.password, args.email)
        client.pretty_print(result)
    
    elif args.command == 'login':
        result = client.login(args.username, args.password)
        client.pretty_print(result)
    
    elif args.command == 'slots':
        result = client.get_slots()
        client.pretty_print(result)
    
    elif args.command == 'book':
        result = client.book_slot(args.slot_id)
        client.pretty_print(result)
    
    elif args.command == 'my-bookings':
        result = client.get_my_bookings()
        client.pretty_print(result)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()