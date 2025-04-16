from django.core.management.base import BaseCommand
from gym.models import Trainer, ClassType, SpecialClassSlot
from django.utils import timezone
import datetime
import random

class Command(BaseCommand):
    help = 'Create sample trainers, class types and special class slots'

    def handle(self, *args, **kwargs):
        # Create trainers with Indian names
        trainers = [
            {'name': 'Aditya Sharma', 'specialization': 'Yoga', 'bio': 'Aditya is a certified yoga instructor with over 5 years of experience in teaching various styles of yoga.'},
            {'name': 'Priya Patel', 'specialization': 'HIIT', 'bio': 'Priya specializes in high-intensity interval training and helps clients achieve their weight loss goals.'},
            {'name': 'Rohit Singh', 'specialization': 'Strength Training', 'bio': 'Rohit is passionate about helping people build muscle and improve overall strength.'},
            {'name': 'Neha Verma', 'specialization': 'Zumba', 'bio': 'Neha brings energy and fun to her Zumba classes, making fitness an enjoyable experience.'},
            {'name': 'Vikram Mehta', 'specialization': 'CrossFit', 'bio': 'Vikram is a certified CrossFit trainer who helps clients push their limits and achieve peak performance.'},
        ]
        
        trainers_created = 0
        trainer_objects = []
        for trainer_data in trainers:
            trainer, created = Trainer.objects.get_or_create(
                name=trainer_data['name'],
                defaults={
                    'specialization': trainer_data['specialization'],
                    'bio': trainer_data['bio']
                }
            )
            if created:
                trainers_created += 1
            trainer_objects.append(trainer)
        
        self.stdout.write(self.style.SUCCESS(f'Created {trainers_created} new trainers'))
        
        # Create class types
        class_types = [
            {'name': 'Yoga', 'description': 'A series of postures and breathing exercises that offer physical and mental benefits.', 'duration_minutes': 60},
            {'name': 'HIIT', 'description': 'High-Intensity Interval Training alternates short periods of intense exercise with less intense recovery periods.', 'duration_minutes': 45},
            {'name': 'Strength Training', 'description': 'Focus on building muscle strength and endurance using weights and resistance equipment.', 'duration_minutes': 60},
            {'name': 'Zumba', 'description': 'A dance fitness program that combines Latin and international music with dance moves.', 'duration_minutes': 50},
            {'name': 'Pilates', 'description': 'A system of exercises designed to improve physical strength, flexibility, and posture.', 'duration_minutes': 55},
        ]
        
        classes_created = 0
        class_type_objects = []
        for class_data in class_types:
            class_type, created = ClassType.objects.get_or_create(
                name=class_data['name'],
                defaults={
                    'description': class_data['description'],
                    'duration_minutes': class_data['duration_minutes']
                }
            )
            if created:
                classes_created += 1
            class_type_objects.append(class_type)
        
        self.stdout.write(self.style.SUCCESS(f'Created {classes_created} new class types'))
        
        # Create special class slots
        if trainer_objects and class_type_objects:
            # Define time slots
            time_slots = [
                ('08:00', '09:00'),
                ('09:00', '10:00'),
                ('10:00', '11:00'),
                ('16:00', '17:00'),
                ('17:00', '18:00'),
                ('18:00', '19:00'),
            ]
            
            # Get dates for the next 7 days
            today = timezone.now().date()
            dates = [today + datetime.timedelta(days=i) for i in range(7)]
            
            slots_created = 0
            
            # Create slots for each date
            for date in dates:
                # For each trainer, create some slots
                for trainer in trainer_objects:
                    # Find matching class type or use any
                    matching_class = next((c for c in class_type_objects if c.name.lower() == trainer.specialization.lower()), 
                                         random.choice(class_type_objects))
                    
                    # Pick 1-2 time slots for this trainer on this day
                    num_slots = random.randint(1, 2)
                    selected_times = random.sample(time_slots, num_slots)
                    
                    for start_time, end_time in selected_times:
                        # Check if the slot already exists
                        slot, created = SpecialClassSlot.objects.get_or_create(
                            date=date,
                            start_time=start_time,
                            end_time=end_time,
                            trainer=trainer,
                            defaults={
                                'class_type': matching_class,
                                'capacity': 8,
                                'available': 8
                            }
                        )
                        if created:
                            slots_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'Created {slots_created} new special class slots'))