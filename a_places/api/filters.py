import django_filters
from rest_framework import serializers

from a_places.models import Workplace
from a_places.api.serializers import DateTimeSerializer
from a_places.services import get_vacant_places


class WorkplaceFilter(django_filters.FilterSet):
    datetime_to = django_filters.IsoDateTimeFromToRangeFilter()
    datetime_from = django_filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Workplace
        fields = [
            'datetime_from',
            'datetime_to',
        ]

    def filter_queryset(self, queryset):
        datetime_from = self.request.GET.get('datetime_from')
        datetime_to = self.request.GET.get('datetime_to')
        if datetime_from and datetime_to:
            serializer = DateTimeSerializer(
                data={
                    'datetime_from': datetime_from,
                    'datetime_to': datetime_to,
                }
            )
            if serializer.is_valid():
                places = get_vacant_places(datetime_from, datetime_to)
                return places
            raise serializers.ValidationError(serializer.errors)
        return Workplace.objects.all()
