import os
import socket
import threading
import datetime
import json
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from gym.models import Slot, Booking

class GymSocketServer:
    """
    A socket-based server to handle gym booking requests.
    Demonstrates raw network programming for the gym booking system.
    """
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.user_sessions = {}  # Maps client addresses to authenticated users
        
    def start(self):
        """Start the socket server."""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Socket server started on {self.host}:{self.port}")
        
        try:
            while True:
                client, address = self.socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client, address))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.socket.close()
    
    def handle_client(self, client, address):
        """Handle client connection and commands."""
        print(f"New connection from {address}")
        
        try:
            while True:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"Received from {address}: {data}")
                response = self.process_command(data, address)
                client.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            if address in self.user_sessions:
                del self.user_sessions[address]
            client.close()
            print(f"Connection closed for {address}")
    
    def process_command(self, command, address):
        """Process the command from the client and return a response."""
        parts = command.strip().split(' ', 1)
        cmd = parts[0].upper()
        
        # Commands that don't require authentication
        if cmd == 'LOGIN':
            if len(parts) < 2:
                return "ERROR: LOGIN requires username and password"
            return self.handle_login(parts[1], address)
        
        if cmd == 'REGISTER':
            if len(parts) < 2:
                return "ERROR: REGISTER requires username, password, and email"
            return self.handle_register(parts[1], address)
        
        # Commands that require authentication
        if address not in self.user_sessions:
            return "ERROR: Authentication required. Please LOGIN first."
        
        user = self.user_sessions[address]
        
        if cmd == 'LIST_SLOTS':
            return self.handle_list_slots()
        
        if cmd == 'BOOK_SLOT':
            if len(parts) < 2:
                return "ERROR: BOOK_SLOT requires a slot ID"
            return self.handle_book_slot(parts[1], user)
        
        if cmd == 'MY_BOOKINGS':
            return self.handle_my_bookings(user)
        
        if cmd == 'LOGOUT':
            del self.user_sessions[address]
            return "SUCCESS: Logged out successfully"
        
        return "ERROR: Unknown command"
    
    def handle_login(self, data, address):
        """Handle LOGIN command."""
        try:
            credentials = json.loads(data)
            username = credentials.get('username')
            password = credentials.get('password')
            
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            
            if user is not None:
                self.user_sessions[address] = user
                return f"SUCCESS: Logged in as {username}"
            else:
                return "ERROR: Invalid credentials"
        except json.JSONDecodeError:
            return "ERROR: Invalid JSON format"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def handle_register(self, data, address):
        """Handle REGISTER command."""
        try:
            user_data = json.loads(data)
            username = user_data.get('username')
            password = user_data.get('password')
            email = user_data.get('email', '')
            
            if not username or not password:
                return "ERROR: Username and password are required"
            
            # Check if user exists
            if User.objects.filter(username=username).exists():
                return "ERROR: Username already taken"
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            return f"SUCCESS: User {username} registered successfully"
        
        except json.JSONDecodeError:
            return "ERROR: Invalid JSON format"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def handle_list_slots(self):
        """Handle LIST_SLOTS command."""
        try:
            today = datetime.date.today()
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
            
            return json.dumps({'slots': slots_data})
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def handle_book_slot(self, data, user):
        """Handle BOOK_SLOT command."""
        try:
            slot_id = int(data.strip())
            
            with transaction.atomic():
                slot = Slot.objects.select_for_update().get(id=slot_id)
                
                if slot.available <= 0:
                    return "ERROR: No available space in this slot"
                
                # Check if user already has a booking
                if Booking.objects.filter(user=user, slot=slot).exists():
                    return "ERROR: You already have a booking for this slot"
                
                # Create booking
                booking = Booking.objects.create(user=user, slot=slot)
                slot.available -= 1
                slot.save()
                
                return f"SUCCESS: Booked slot on {slot.date} from {slot.start_time} to {slot.end_time}"
                
        except Slot.DoesNotExist:
            return "ERROR: Slot not found"
        except ValueError:
            return "ERROR: Invalid slot ID format"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def handle_my_bookings(self, user):
        """Handle MY_BOOKINGS command."""
        try:
            bookings = Booking.objects.filter(user=user).select_related('slot')
            
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
            
            return json.dumps({'bookings': bookings_data})
        except Exception as e:
            return f"ERROR: {str(e)}"

if __name__ == "__main__":
    server = GymSocketServer()
    server.start()