from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets

from vehicle.models import Car, Milage, Moto
from vehicle.paginators import VehiclePaginator
from vehicle.permissions import IsOwnerOrStaff
from vehicle.serliazers import (CarSerializer, MilageSerializer,
                                MotoMilageSerializer, MotoSerializer,
                                MotoCreateSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()  # На случай если нужно выводить активные или
    # неактивные элементы, или это ViewSet, для работы с пользователями одного
    # какого то типа

    # Если активируем аутентификацию вторым способом, то в контроллер добавляем
    # permission_classes
    permission_classes = [AllowAny]

    # Если бы пришлось сделать, отдельный serializer для CarViewSet
    # def post(self, *args, **kwargs):
    #     self.serializer_class =CarCreateSerializer
    #     super()

    def create(self, request, *args, **kwargs):
        """Для автоматического добавления пользователя нужно сделать то же
        самое, что в MotoCreateAPIView в методе perform_create"""
        pass


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Для автоматического добавления пользователя"""
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()


class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    permission_classes = [IsOwnerOrStaff]


class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MotoMilageListAPIView(generics.ListAPIView):
    queryset = Milage.objects.filter(moto__isnull=False)  # moto__isnull=False -
    # это условие, чтобы мотоциклы были заполнены для всего этого пробега
    serializer_class = MotoMilageSerializer


class MilageCreateAPIView(generics.CreateAPIView):
    serializer_class = MilageSerializer


class MilageListAPIView(generics.ListAPIView):
    queryset = Milage.objects.all()
    serializer_class = MilageSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('car', 'moto',)
    ordering_fields = ('year',)

    # Есть возможность добавить функционал по поиску
    # search_fields = ('car',)
