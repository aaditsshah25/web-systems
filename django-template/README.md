# Gym Booking System

This Django project provides a comprehensive gym booking system with both web and socket-based interfaces. Users can register, log in, view available slots, book gym sessions, and register for special classes with trainers.

Developed as part of a Web Systems course assignment under the guidance of **Prof. Aamod Sane** at **FLAME University**.

---

## Contributors
- Aadit Shah
- Neel Patel

---

## Features
- **User Authentication** — Register and login securely
- **Regular Gym Bookings** — Browse and book available gym slots
- **Special Classes** — Book sessions with expert trainers
- **Calendar View** — Visualize slot availability
- **Trainer Profiles** — View trainer specializations and experience
- **Admin Dashboard** — Complete management interface for gym administrators
- **Dual Interfaces** — Web UI and Socket API for programmatic access
- **Real-time Updates** — Track slot availability as changes occur

---

## Requirements
- Python 3.11 or higher
- Django 5.0.4
- Pillow (for image processing)
- Other dependencies listed in `requirements.txt`

---

## Setup and Installation

### Prerequisites
We recommend installing the following VS Code extensions:
- **Python**
- **Python Debugger**
- **Pylance**

### Installation Steps
1. Clone this repository to your local machine.
2. Open the project folder in VS Code (`File > Open Folder...`).
3. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Recommended Method: Using `run_system.py`
Run the complete system easily via:

```bash
python run_system.py
```

This script automatically:
- Sets up the database (migrations)
- Creates a superuser if needed
- Initializes gym slots
- Creates trainers and special classes
- Starts both Django web server and Socket server
- Opens the browser to the selected interface

### Manual Method
Alternatively, you can run components separately:

1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Create gym slots:
   ```bash
   python -m gym.createslots
   ```

4. Create trainers and special classes:
   ```bash
   python manage.py create_trainers_classes
   ```

5. Start the Django web server:
   ```bash
   python manage.py runserver
   ```

6. In a new terminal, run the Socket server:
   ```bash
   python -m gym.socket_server
   ```

---

## User Credentials
- **Admin**: A default admin user is created during setup
  - Username: `admin`
  - Password: `flamecsit*`
- **Regular User**: Register a new user via the web interface.

---

## System Components

### Web Interface
- **URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Key Features**:
  - User registration and login
  - Dashboard for managing bookings
  - Regular gym slot booking
  - Special class booking with trainers
  - Calendar view for slot availability
  - Trainer profiles and details

### Admin Interface
- **URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Admin Features**:
  - Manage gym slots and capacities
  - Manage trainers and special classes
  - View and modify user bookings
  - Configure system settings

### API Interfaces
- **REST API** — Access via HTTP endpoints
- **Socket API** — Connects to `127.0.0.1:8888`

**Client Libraries**:
- `gym.socket_client.py` — For Socket API communication
- `gym.api_client.py` — For REST API communication

---

## Project Structure

```bash
project/
├── gym/                  # Main application code
│   ├── models.py         # Database models
│   ├── views.py          # View controllers
│   ├── templates/        # HTML templates
│   ├── static/           # CSS and JavaScript files
│   └── management/       # Custom management commands
├── web_django/           # Django project configuration
└── run_system.py         # Utility script to run the entire system
```

---

## Testing

To run all tests:

```bash
python manage.py test
```

---

## Notes
- Make sure to keep your `requirements.txt` updated if new dependencies are added.
- If you encounter any issues during setup, ensure that ports `8000` (HTTP) and `8888` (Socket) are free.
- Always activate your virtual environment when working with the project.

---

_This project demonstrates an integrated web system, combining high-level web development with low-level socket communication for a complete and scalable booking platform._
