from django.db import models
from django.urls import reverse
from django.db.models import Q

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    location = models.CharField(max_length=255, verbose_name="Местоположение")
    rating = models.FloatField(verbose_name="Рейтинг")
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость за ночь")
    image = models.ImageField(
        upload_to='hotel_images/', verbose_name="Изображение", null=True, blank=True)

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotel_detail', args=[str(self.id)])


class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Стандарт'),
        ('Luxury', 'Люкс'),
        ('Apartment', 'Апартаменты'),
    ]

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, verbose_name="Отель")
    room_number = models.CharField(
        max_length=10, verbose_name="Номер комнаты", unique=True, null=True, blank=True)
    room_type = models.CharField(
        max_length=50, choices=ROOM_TYPES, verbose_name="Тип номера")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    available = models.BooleanField(default=True, verbose_name="Доступность")
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость за ночь", default=100.00)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ['room_number']

    def __str__(self):
        return f"{self.hotel.name} - Номер {self.room_number}"

    def is_available(self, check_in, check_out):
        overlapping_bookings = Reservation.objects.filter(
            room=self,
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        return not overlapping_bookings.exists()


class Reservation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, verbose_name='Комната')
    check_in = models.DateField(verbose_name='Дата заезда')
    check_out = models.DateField(verbose_name='Дата выезда')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.room.hotel.name} - {self.room.room_type}"

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.username} об отеле {self.hotel.name}'
