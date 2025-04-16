from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Slot(models.Model):
    """Model representing a gym time slot."""
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField(default=10)
    available = models.IntegerField(default=10)
    
    def __str__(self):
        return f"{self.date} - {self.start_time} to {self.end_time}"
    
    class Meta:
        unique_together = ('date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']

class Booking(models.Model):
    """Model representing a booking made by a user for a specific slot."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.slot}"
    
    class Meta:
        unique_together = ('user', 'slot')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # Removed profile_picture field
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Trainer(models.Model):
    """Model representing a gym trainer."""
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='trainer_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.specialization})"

class ClassType(models.Model):
    """Model representing a type of fitness class."""
    name = models.CharField(max_length=100)  # e.g., Yoga, HIIT, Weights, Zumba
    description = models.TextField()
    duration_minutes = models.IntegerField(default=60)
    
    def __str__(self):
        return self.name

class SpecialClassSlot(models.Model):
    """Model representing a special class slot with a trainer."""
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE, related_name='slots')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='slots')
    capacity = models.IntegerField(default=10)
    available = models.IntegerField(default=10)
    
    def __str__(self):
        return f"{self.class_type} with {self.trainer} on {self.date} at {self.start_time}"
    
    class Meta:
        unique_together = ('date', 'start_time', 'trainer')
        ordering = ['date', 'start_time']

class TrainerBooking(models.Model):
    """Model representing a booking for a special class."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_bookings')
    class_slot = models.ForeignKey(SpecialClassSlot, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.class_slot}"
    
    class Meta:
        unique_together = ('user', 'class_slot')