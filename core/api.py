from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Historic
from core.serializers import (
    CreateParkingSerializer,
    ListParkingSerializer,
    UpdateParkingSerializer
)


class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Historic.objects.all()
    serializer_class = ListParkingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["plate"]
    http_method_names = ['get', 'post', 'patch']

    @action(methods=["patch"], detail=True)
    def checkout(self, request, pk=None, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(methods=["patch"], detail=True)
    def out(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()

        if not instance.paid:
            return Response(
                data="A saída só pode ser registrada depois que o pagamento for efetuado.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.partial_update(request, *args, **kwargs)

    def get_serializer_class(self):
        serializers = {
            "list": ListParkingSerializer,
            "create": CreateParkingSerializer,
            "checkout": UpdateParkingSerializer,
            "out": UpdateParkingSerializer,
        }
        try:
            return serializers[self.action]
        except KeyError:
            return super().get_serializer_class()
