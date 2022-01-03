from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Workplace(models.Model):

    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

    def __str__(self):
        return f'Рабочее место №{self.id}'


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.ForeignKey(Workplace, on_delete=models.CASCADE, verbose_name='Рабочее место')
    datetime_from = models.DateTimeField('Время начала бронирования')
    datetime_to = models.DateTimeField('Время окончания бронирования')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Бронь'

    def __str__(self):
        return f'С {self.datetime_from.time()} по {self.datetime_to.time()}'
