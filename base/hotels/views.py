from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Hotel, Room, Reservation, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from decimal import Decimal
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.


def index(request):
    # Показываем только 6 отелей на главной
    featured_hotels = Hotel.objects.all()[:6]
    return render(request, 'hotels/index.html', {'featured_hotels': featured_hotels})


def hotel_search(request):
    hotels = Hotel.objects.all()

    # Поиск по ключевым словам
    keyword = request.GET.get('keyword')
    if keyword:
        hotels = hotels.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # Фильтр по местоположению
    location = request.GET.get('location')
    if location:
        hotels = hotels.filter(location__icontains=location)

    # Фильтр по рейтингу
    rating = request.GET.get('rating')
    if rating:
        hotels = hotels.filter(rating__gte=rating)

    # Фильтр по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        hotels = hotels.filter(price_per_night__gte=min_price)
    if max_price:
        hotels = hotels.filter(price_per_night__lte=max_price)

    return render(request, 'hotels/hotels_search.html', {'hotels': hotels})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})


@login_required
def book_room(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, id=room_id)
        try:
            check_in = datetime.strptime(
                request.POST['check_in'], '%Y-%m-%d').date()
            check_out = datetime.strptime(
                request.POST['check_out'], '%Y-%m-%d').date()

            # Проверка корректности дат
            if check_in >= check_out:
                messages.error(
                    request, 'Дата выезда должна быть позже даты заезда')
                return redirect('hotel_detail', pk=room.hotel.id)

            if check_in < datetime.now().date():
                messages.error(request, 'Дата заезда не может быть в прошлом')
                return redirect('hotel_detail', pk=room.hotel.id)

            # Проверка доступности номера
            if not room.is_available(check_in, check_out):
                messages.error(request, 'Номер недоступен на выбранные даты')
                return redirect('hotel_detail', pk=room.hotel.id)

            # Расчет общей стоимости
            days = (check_out - check_in).days
            total_price = room.price_per_night * Decimal(days)

            # Создание бронирования
            reservation = Reservation.objects.create(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price
            )

            messages.success(request, 'Бронирование успешно создано')
            return redirect('user_bookings')

        except ValueError:
            messages.error(request, 'Неверный формат даты')
            return redirect('hotel_detail', pk=room.hotel.id)
        except Exception as e:
            messages.error(request, f'Ошибка при бронировании: {str(e)}')
            return redirect('hotel_detail', pk=room.hotel.id)

    return redirect('hotel_detail', pk=room.hotel.id)


@login_required
def user_bookings(request):
    bookings = Reservation.objects.filter(
        user=request.user).order_by('-check_in')
    today = datetime.now().date()
    return render(request, 'hotels/user_bookings.html', {
        'bookings': bookings,
        'today': today
    })


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена')
            return redirect('index')
    else:
        form = UserCreationForm()

    # Добавляем классы Bootstrap к полям формы
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'hotels/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('index')
    else:
        form = AuthenticationForm()

    # Добавляем классы Bootstrap к полям формы
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'hotels/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')


@login_required
def add_review(request, hotel_id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            Review.objects.create(
                user=request.user,
                hotel=hotel,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Спасибо за ваш отзыв!')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля')

        return redirect('hotel_detail', pk=hotel_id)
