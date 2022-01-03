from django.contrib import admin

from .models import Workplace, Reservation


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'place',
        'datetime_from',
        'datetime_to',
    ]
    list_editable = [
        'datetime_from',
        'datetime_to',
        'place',
    ]
