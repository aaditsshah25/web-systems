import os
import sys
import subprocess
import time
import webbrowser
import signal
import threading
import django

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import django
        import requests
    except ImportError:
        print("Installing dependencies...")
        os.system("pip install django requests")
        time.sleep(1)

def setup_database():
    """Run migrations and create initial data."""
    print("Setting up database...")
    os.system("python manage.py migrate")
    
    # Check if superuser exists or create one
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        print("\n=== Creating admin superuser ===")
        os.system("python manage.py createsuperuser")
    
    # Check if slots exist or create them
    from gym.models import Slot
    if Slot.objects.count() == 0:
        print("\n=== Creating initial gym slots ===")
        os.system("python -m gym.createslots")
    
    print("\nDatabase setup complete!")

# Global variables to store server processes
django_process = None
socket_process = None

def run_django_server():
    """Run the Django server as a background process."""
    global django_process
    print("Starting Django server...")
    
    if os.name == 'nt':  # Windows
        django_process = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    else:  # Linux/Mac
        django_process = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    # Create a thread to monitor and log server output
    def monitor_output():
        for line in iter(django_process.stdout.readline, b''):
            print(f"Django: {line.decode().strip()}")
    
    threading.Thread(target=monitor_output, daemon=True).start()

def run_socket_server():
    """Run the Socket server as a background process."""
    global socket_process
    print("Starting Socket server...")
    
    if os.name == 'nt':  # Windows
        socket_process = subprocess.Popen(
            ["python", "-m", "gym.socket_server"],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    else:  # Linux/Mac
        socket_process = subprocess.Popen(
            ["python", "-m", "gym.socket_server"],
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    # Create a thread to monitor and log server output
    def monitor_output():
        for line in iter(socket_process.stdout.readline, b''):
            print(f"Socket: {line.decode().strip()}")
    
    threading.Thread(target=monitor_output, daemon=True).start()

def run_all():
    """Run the entire system with servers in background."""
    # Start Django server as a background process
    run_django_server()
    
    # Give Django server time to start
    time.sleep(2)
    
    # Start Socket server as a background process
    run_socket_server()
    
    time.sleep(1)
    
    # Ask user which interface they want to open
    print("\nWhich interface would you like to open?")
    print("1. User interface (for gym members)")
    print("2. Admin interface (for administrators)")
    print("3. Both interfaces")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            print("Opening user interface in browser...")
            webbrowser.open("http://127.0.0.1:8000/")
            break
        elif choice == '2':
            print("Opening admin interface in browser...")
            webbrowser.open("http://127.0.0.1:8000/admin/")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    print("\nServers are running in the background.")
    print("Press Ctrl+C to stop all servers and exit.")
    
    # Keep the main process running until Ctrl+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

def cleanup():
    """Stop all server processes."""
    print("\nStopping servers...")
    
    if django_process:
        if os.name == 'nt':  # Windows
            os.kill(django_process.pid, signal.CTRL_BREAK_EVENT)
        else:  # Linux/Mac
            os.killpg(os.getpgid(django_process.pid), signal.SIGTERM)
    
    if socket_process:
        if os.name == 'nt':  # Windows
            os.kill(socket_process.pid, signal.CTRL_BREAK_EVENT)
        else:  # Linux/Mac
            os.killpg(os.getpgid(socket_process.pid), signal.SIGTERM)
    
    print("All servers stopped.")

def main():
    """Main function."""
    clear_screen()
    print("=== Gym Booking System Runner ===\n")
    
    # Ensure the script is run from the django-template directory
    if not os.path.exists('manage.py'):
        print("Error: This script must be run from the django-template directory.")
        print("Please navigate to the django-template directory and try again.")
        return
    
    # Check dependencies
    check_dependencies()
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.settings')
    import django
    django.setup()
    
    # Setup database
    setup_database()
    
    # Ask user if they want to run the system
    print("\nSetup complete! Ready to run the system.")
    # response = input("Start all servers now? (y/n): ").lower()
    
    # if response == 'y':
    run_all()
    # else:
    #     print("\nTo run the system manually:")
    #     print("1. Start Django server: python manage.py runserver")
    #     print("2. Start Socket server: python -m gym.socket_server")
    #     print("3. Use API client: python -m gym.api_client <command>")
    #     print("4. Use Socket client: python -m gym.socket_client <command>")

if __name__ == "__main__":
    main()