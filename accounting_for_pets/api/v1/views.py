from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.v1.serializers import PetCreateSerializer, PetSerializer
from pets.models import Pet


class PetViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """."""

    queryset = Pet.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return PetCreateSerializer
        return PetSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"count": queryset.count(), "items": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
