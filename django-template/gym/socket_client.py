import socket
import json
import argparse

class GymSocketClient:
    """Client for interacting with the Socket-based Gym Booking Server."""
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Connect to the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
    
    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected from server")
    
    def send_command(self, command):
        """Send a command to the server and return the response."""
        if not self.socket:
            self.connect()
        
        self.socket.send(command.encode('utf-8'))
        response = self.socket.recv(4096).decode('utf-8')
        return response
    
    def register(self, username, password, email=None):
        """Register a new user."""
        data = {
            'username': username,
            'password': password,
        }
        if email:
            data['email'] = email
            
        command = f"REGISTER {json.dumps(data)}"
        return self.send_command(command)
    
    def login(self, username, password):
        """Login a user."""
        data = {
            'username': username,
            'password': password,
        }
        
        command = f"LOGIN {json.dumps(data)}"
        return self.send_command(command)
    
    def list_slots(self):
        """List available slots."""
        command = "LIST_SLOTS"
        response = self.send_command(command)
        
        # Try to pretty-print JSON if the response is valid JSON
        try:
            data = json.loads(response)
            return json.dumps(data, indent=4)
        except json.JSONDecodeError:
            return response
    
    def book_slot(self, slot_id):
        """Book a slot."""
        command = f"BOOK_SLOT {slot_id}"
        return self.send_command(command)
    
    def my_bookings(self):
        """Get user's bookings."""
        command = "MY_BOOKINGS"
        response = self.send_command(command)
        
        # Try to pretty-print JSON if the response is valid JSON
        try:
            data = json.loads(response)
            return json.dumps(data, indent=4)
        except json.JSONDecodeError:
            return response
    
    def logout(self):
        """Logout the current user."""
        command = "LOGOUT"
        return self.send_command(command)

def main():
    """Command-line interface for the socket client."""
    parser = argparse.ArgumentParser(description='Gym Booking System Socket Client')
    parser.add_argument('--host', default='127.0.0.1',
                      help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8888,
                      help='Server port (default: 8888)')
    
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
    
    # List slots command
    subparsers.add_parser('list-slots', help='List available slots')
    
    # Book command
    book_parser = subparsers.add_parser('book', help='Book a slot')
    book_parser.add_argument('slot_id', type=int, help='Slot ID to book')
    
    # My bookings command
    subparsers.add_parser('my-bookings', help='List my bookings')
    
    # Logout command
    subparsers.add_parser('logout', help='Logout current user')
    
    args = parser.parse_args()
    client = GymSocketClient(host=args.host, port=args.port)
    
    try:
        if args.command == 'register':
            result = client.register(args.username, args.password, args.email)
            print(result)
        
        elif args.command == 'login':
            result = client.login(args.username, args.password)
            print(result)
        
        elif args.command == 'list-slots':
            result = client.list_slots()
            print(result)
        
        elif args.command == 'book':
            result = client.book_slot(args.slot_id)
            print(result)
        
        elif args.command == 'my-bookings':
            result = client.my_bookings()
            print(result)
        
        elif args.command == 'logout':
            result = client.logout()
            print(result)
        
        else:
            parser.print_help()
    
    finally:
        client.disconnect()

if __name__ == '__main__':
    main()