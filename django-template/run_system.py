import os
import sys
import subprocess
import time
import webbrowser

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

def run_all():
    """Run the entire system with multiple terminals."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Start Django server in a new terminal
    print("Starting Django server...")
    if os.name == 'nt':  # Windows
        django_cmd = f'start cmd /k "cd /d {project_dir} && python manage.py runserver"'
    else:  # Linux/Mac
        django_cmd = f'gnome-terminal -- bash -c "cd {project_dir} && python manage.py runserver; bash"'
    os.system(django_cmd)
    
    # Give Django server time to start
    time.sleep(2)
    
    # Start Socket server in a new terminal
    print("Starting Socket server...")
    if os.name == 'nt':  # Windows
        socket_cmd = f'start cmd /k "cd /d {project_dir} && python -m gym.socket_server"'
    else:  # Linux/Mac
        socket_cmd = f'gnome-terminal -- bash -c "cd {project_dir} && python -m gym.socket_server; bash"'
    os.system(socket_cmd)
    
    # Open admin in browser
    print("Opening admin interface in browser...")
    webbrowser.open("http://127.0.0.1:8000/admin/")
    
    # Open a terminal for API client demos
    print("Opening terminal for API client...")
    if os.name == 'nt':  # Windows
        api_client_cmd = f'start cmd /k "cd /d {project_dir} && echo API Client Commands: && echo python -m gym.api_client register testuser password && echo python -m gym.api_client login testuser password && echo python -m gym.api_client slots && echo python -m gym.api_client book 1 && echo python -m gym.api_client my-bookings"'
    else:  # Linux/Mac
        api_client_cmd = f'gnome-terminal -- bash -c "cd {project_dir} && echo API Client Commands: && echo python -m gym.api_client register testuser password && echo python -m gym.api_client login testuser password && echo python -m gym.api_client slots && echo python -m gym.api_client book 1 && echo python -m gym.api_client my-bookings; bash"'
    os.system(api_client_cmd)
    
    # Open a terminal for Socket client demos
    print("Opening terminal for Socket client...")
    if os.name == 'nt':  # Windows
        socket_client_cmd = f'start cmd /k "cd /d {project_dir} && echo Socket Client Commands: && echo python -m gym.socket_client register testuser2 password && echo python -m gym.socket_client login testuser2 password && echo python -m gym.socket_client list-slots && echo python -m gym.socket_client book 1 && echo python -m gym.socket_client my-bookings"'
    else:  # Linux/Mac
        socket_client_cmd = f'gnome-terminal -- bash -c "cd {project_dir} && echo Socket Client Commands: && echo python -m gym.socket_client register testuser2 password && echo python -m gym.socket_client login testuser2 password && echo python -m gym.socket_client list-slots && echo python -m gym.socket_client book 1 && echo python -m gym.socket_client my-bookings; bash"'
    os.system(socket_client_cmd)

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
    response = input("Start all servers now? (y/n): ").lower()
    
    if response == 'y':
        run_all()
        print("\nAll components are now running!")
        print("\nTo stop all servers, close the terminal windows or press Ctrl+C in each.")
    else:
        print("\nTo run the system manually:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Start Socket server: python -m gym.socket_server")
        print("3. Use API client: python -m gym.api_client <command>")
        print("4. Use Socket client: python -m gym.socket_client <command>")

# ...existing code...

def run_all():
    """Run the entire system with multiple terminals."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Start Django server in a new terminal
    print("Starting Django server...")
    if os.name == 'nt':  # Windows
        django_cmd = f'start cmd /k "cd /d {project_dir} && python manage.py runserver"'
    else:  # Linux/Mac
        django_cmd = f'gnome-terminal -- bash -c "cd {project_dir} && python manage.py runserver; bash"'
    os.system(django_cmd)
    
    # Give Django server time to start
    time.sleep(2)
    
    # Start Socket server in a new terminal
    print("Starting Socket server...")
    if os.name == 'nt':  # Windows
        socket_cmd = f'start cmd /k "cd /d {project_dir} && python -m gym.socket_server"'
    else:  # Linux/Mac
        socket_cmd = f'gnome-terminal -- bash -c "cd {project_dir} && python -m gym.socket_server; bash"'
    os.system(socket_cmd)
    
    # ...existing code...

    # Open client website in browser
    print("Opening client website in browser...")
    webbrowser.open("http://127.0.0.1:8000/")  # Changed from /api/ to /
    
    # Open admin in browser
    print("Opening admin interface in browser...")
    webbrowser.open("http://127.0.0.1:8000/admin/")
    
    # ...rest of existing code...

if __name__ == "__main__":
    main()