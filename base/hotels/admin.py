from django.contrib import admin
from .models import Hotel, Room, Reservation, Review


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type',
                    'capacity', 'price_per_night', 'available')
    list_filter = ('hotel', 'room_type', 'available')
    search_fields = ('room_number', 'hotel__name')
    ordering = ('hotel', 'room_number')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price_per_night')
    search_fields = ('name', 'location')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'total_price')
    list_filter = ('check_in', 'check_out')
    search_fields = ('user__username', 'room__hotel__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'hotel')
    search_fields = ('user__username', 'hotel__name', 'comment')
