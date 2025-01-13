from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hotels.models import Hotel, Room
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Creates test data for the hotel booking system'

    def handle(self, *args, **kwargs):
        # Создаем тестового суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Создаем отели
        hotels_data = [
            {
                'name': 'Гранд Отель',
                'description': 'Роскошный отель в центре города с видом на парк',
                'location': 'Москва',
                'rating': 4.8,
                'price_per_night': Decimal('5000.00')
            },
            {
                'name': 'Морской Бриз',
                'description': 'Уютный отель на берегу моря',
                'location': 'Сочи',
                'rating': 4.5,
                'price_per_night': Decimal('4000.00')
            },
            {
                'name': 'Горный Курорт',
                'description': 'Отель в горах с видом на вершины',
                'location': 'Красная Поляна',
                'rating': 4.6,
                'price_per_night': Decimal('4500.00')
            }
        ]

        for hotel_data in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Hotel "{hotel.name}" created'))

                # Создаем номера для каждого отеля
                room_types = ['Standard', 'Luxury', 'Apartment']
                floor = 1
                for room_type in room_types:
                    # 3 номера каждого типа
                    for i in range(3):
                        room_number = f"{floor}{i+1}"
                        price_multiplier = 1 if room_type == 'Standard' else (
                            1.5 if room_type == 'Luxury' else 2)
                        capacity = 2 if room_type == 'Standard' else (
                            3 if room_type == 'Luxury' else 4)

                        Room.objects.create(
                            hotel=hotel,
                            room_number=f"{hotel.id}{room_number}",
                            room_type=room_type,
                            capacity=capacity,
                            price_per_night=hotel.price_per_night * price_multiplier,
                            available=True
                        )
                    floor += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Rooms created for "{hotel.name}"'))

        self.stdout.write(self.style.SUCCESS('Test data created successfully'))
