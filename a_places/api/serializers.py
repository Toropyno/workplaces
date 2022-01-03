from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from a_places.services import get_reservation_on_period
from a_places.models import Workplace, Reservation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
        ]


class WorkplaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Workplace
    """
    url = serializers.HyperlinkedIdentityField(view_name='workplace-detail')

    class Meta:
        model = Workplace
        fields = [
            'id',
            'url',
        ]


class ReservationSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Reservation
    """
    url = serializers.HyperlinkedIdentityField(view_name='reservation-detail')

    class Meta:
        model = Reservation
        fields = [
            'user',
            'place',
            'datetime_from',
            'datetime_to',
            'url',
        ]

    def validate(self, attrs):
        datetime_from = attrs.get('datetime_from')
        datetime_to = attrs.get('datetime_to')
        if datetime_from >= datetime_to:
            raise serializers.ValidationError('Некорректный отрезок времени: значение поля datetime_to должно быть больше значения поля datetime_from.')
        else:
            if datetime_from < timezone.now():
                raise serializers.ValidationError('Некорректный отрезок времени: значение поля datetime_from должно быть больше текущей даты и времени')
            return super().validate(attrs)

    def create(self, validated_data):
        datetime_from = validated_data.get('datetime_from')
        datetime_to = validated_data.get('datetime_to')
        place = validated_data.get('place')

        has_reserve = get_reservation_on_period(datetime_from, datetime_to, place)
        if has_reserve:
            raise serializers.ValidationError(
                'Ошибка при бронировании: место занято в данный отрезок времени.')
        return super().create(validated_data)


class ReservePlaceSerializer(ReservationSerializer):
    """
    Сериализатор для бронирования определенного рабочего места

    Расширение базового класса ReservationSerializer:
    * автоматически заполняет поля user и place (данные берутся из request.data);
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    place = serializers.PrimaryKeyRelatedField(read_only=True)


class DateTimeSerializer(serializers.Serializer):
    """
    Сериализатор даты и времени

    * используется как валидатор значений datetime_from и datetime_to
    """
    datetime_from = serializers.DateTimeField()
    datetime_to = serializers.DateTimeField()

    def validate(self, attrs):
        datetime_from = attrs.get('datetime_from')
        datetime_to = attrs.get('datetime_to')
        if datetime_from >= datetime_to:
            raise serializers.ValidationError('Некорректный отрезок времени: значение поля datetime_to должно быть больше значения поля datetime_from.')
        return super().validate(attrs)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
