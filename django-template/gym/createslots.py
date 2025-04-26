import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.settings')
django.setup()

from gym.models import Slot

def create_slots():
    """Create sample gym slots for the next 21 days (3 weeks)."""
    print("Creating gym slots...")
    
    # Define time slots
    time_slots = [
        ('08:00', '09:00'),
        ('09:00', '10:00'),
        ('10:00', '11:00'),
        ('16:00', '17:00'),
        ('17:00', '18:00'),
        ('18:00', '19:00'),
    ]
    
    # Get dates for the next 21 days (3 weeks)
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=i) for i in range(21)]
    
    slots_created = 0
    
    # Create slots for each date and time combination
    for date in dates:
        for start_time, end_time in time_slots:
            # Check if the slot already exists
            if not Slot.objects.filter(
                date=date,
                start_time=start_time,
                end_time=end_time
            ).exists():
                # Create the slot
                Slot.objects.create(
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    capacity=10,
                    available=10
                )
                slots_created += 1
    
    print(f"Created {slots_created} new gym slots.")

if __name__ == "__main__":
    create_slots()