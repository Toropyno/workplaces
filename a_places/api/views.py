from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import (ReservationSerializer,
                          WorkplaceSerializer,
                          UserSerializer,
                          ReservePlaceSerializer, )
from a_places.api.filters import WorkplaceFilter
from a_places.models import Reservation, Workplace


class WorkplaceViewSet(viewsets.ModelViewSet):
    """
    Рабочие места

    * разрешены методы: чтение;
    * только для авторизованных пользователей;
    """
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkplaceFilter

    @action(detail=True)
    def reservations(self, request, pk=None):
        """
        Список бронирований рабочего места

        * только для авторизованных пользователей;
        """
        reservations = Reservation.objects.filter(place=self.get_object())
        serializer = ReservationSerializer(reservations, many=True, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        actions_for_admin_only = ['create', 'update', 'partial_update', 'destroy']
        if self.action in actions_for_admin_only:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ReservationViewSet(viewsets.ModelViewSet):
    """
    Бронирования

    * разрешены методы: чтение, удаление;
    * только для авторизованных пользователей;
    """
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user']

    def get_permissions(self):
        actions_for_admin_only = ['update', 'partial_update', 'create']
        if self.action in actions_for_admin_only:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)


class CreateReservationView(generics.CreateAPIView):
    """
    Бронирование рабочего места

    * бронирует рабочее место;
    * разрешены методы: запись;
    * только для авторизованных пользователей;
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservePlaceSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.pk
        data['place'] = kwargs.get('pk')

        serializer = ReservationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserViewSet(viewsets.ModelViewSet):
    """
    Пользователи

    * разрешены методы: запись;
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        actions_for_admin_only = ['retrieve', 'list', 'update', 'partial_update', 'destroy']
        if self.action in actions_for_admin_only:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
