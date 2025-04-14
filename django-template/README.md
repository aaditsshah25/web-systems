# Gym Booking System

This Django project provides a comprehensive gym booking system with both web and socket-based interfaces. Users can register, log in, view available slots, and book gym sessions. This project was developed as part of a college project under the guidance of Prof. Aamod Sane at FLAME University.

## Contributors

- Aadit Shah
- Neel Patel

## Features

- User registration and authentication
- Web interface for browsing and booking gym slots
- Socket-based API for programmatic access
- Admin interface for gym managers
- Real-time slot availability tracking

## Requirements

- Python 3.11 or higher
- Django 5.0.4
- Other dependencies listed in `requirements.txt`

## Setup and Installation

To successfully run this application, we recommend the following VS Code extensions:
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

Installation steps:
1. Open the project folder in VS Code (**File** > **Open Folder...**)
2. Create a Python virtual environment using the **Python: Create Environment** command found in the Command Palette (**View > Command Palette**). Ensure you install dependencies found in the `requirements.txt` file
3. Ensure your newly created environment is selected using the **Python: Select Interpreter** command found in the Command Palette

## Running the Application

### Recommended Method: Using run_system.py

The easiest way to run the complete system is using the `run_system.py` script, which will:
- Set up the database (run migrations)
- Create a superuser if needed
- Create initial gym slots if needed
- Start both the Django web server and the Socket server
- Open your browser to the selected interface

```bash
python run_system.py
```

### Manual Method

If you prefer to run components separately:

1. Create and initialize the database:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser (if needed):
   ```bash
   python manage.py createsuperuser
   ```

3. Create initial gym slots:
   ```bash
   python -m gym.createslots
   ```

4. Run the Django web server:
   ```bash
   python manage.py runserver
   ```

5. In a separate terminal, run the Socket server:
   ```bash
   python -m gym.socket_server
   ```

## Testing

Run tests with:
```bash
python manage.py test
```

## Project Structure

- `gym/` - Main application with models, views, and templates
- `web_django/` - Django project configuration
- `run_system.py` - Utility script to run the entire system

## Using the System

- Web Interface: http://127.0.0.1:8000/
- Admin Interface: http://127.0.0.1:8000/admin/
- Socket API: Connects to 127.0.0.1:8888

You can use the web interface directly in your browser, or interact with the system programmatically using:
- `gym.socket_client.py` - Client for the socket API
- `gym.api_client.py` - Client for the REST API