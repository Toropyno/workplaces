from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Workplace, Reservation

User = get_user_model()


def get_vacant_places(datetime_from, datetime_to):
    """
    Возвращает список свободных рабочих мест в заданный период времени

    * получает список бронирований в заданный отрезок времени и на его основе формирует  список свободных рабочих мест
    """
    reservation_list = get_reservation_on_period(datetime_from, datetime_to)

    if reservation_list:
        reserved_places = reservation_list.values_list('place', flat=True)
        return Workplace.objects.exclude(pk__in=reserved_places)
    return Workplace.objects.all()


def get_reservation_on_period(datetime_from, datetime_to, place=None):
    """
    Возвращает список бронирований на данный промежуток времени
    """
    reservation_list = Reservation.objects.exclude(
        Q(datetime_to__lt=datetime_from) | Q(datetime_from__gt=datetime_to)
    )
    if place:
        return reservation_list.filter(place=place)

    return reservation_list
