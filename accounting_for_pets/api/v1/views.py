import os

from django.conf import settings
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.v1.serializers import PetSerializer, PhotoUploadSerializer
from pets.models import Pet


class PetViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """ViewSet для управления объектами модели Pet."""

    queryset = Pet.objects.all()

    def get_serializer_class(self) -> type:
        """
        Возвращает класс сериализатора в зависимости от действия.

        Возвращает:
            type: Класс сериализатора.
        """
        if self.action == "upload_photo":
            return PhotoUploadSerializer
        return PetSerializer

    def list(self, request) -> Response:
        """
        Возвращает список объектов Pet с возможностью фильтрации и пагинации.

        Аргументы:
            request (Request): HTTP запрос.

        Возвращает:
            Response: HTTP ответ с данными списка объектов.
        """
        queryset = self.get_queryset()

        limit = request.query_params.get("limit", settings.PAGINATION_LIMIT)
        offset = request.query_params.get("offset", settings.PAGINATION_OFFSET)
        has_photos = request.query_params.get(
            "has_photos", settings.HAS_PHOTOS_DEFAULT
        )

        try:
            limit = int(limit)
            offset = int(offset)
        except ValueError:
            return Response(
                {"error": "Invalid limit or offset"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if has_photos is not None:
            if has_photos.lower() == "true":
                queryset = queryset.filter(photos__isnull=False).distinct()
            elif has_photos.lower() == "false":
                queryset = queryset.filter(photos__isnull=True)

        total_count = queryset.count()
        queryset = queryset[offset : offset + limit]

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )

        return Response({"count": total_count, "items": serializer.data})

    def create(self, request) -> Response:
        """
        Создает новый объект Pet.

        Аргументы:
            request (Request): HTTP запрос.

        Возвращает:
            Response: HTTP ответ с данными созданного объекта.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        pet = Pet.objects.get(id=serializer.data["id"])
        full_serializer = self.get_serializer(
            pet, context={"request": request}
        )
        return Response(
            full_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        detail=True,
        methods=["post"],
        parser_classes=[MultiPartParser, FormParser],
        url_path="photo",
    )
    def upload_photo(self, request, pk=None) -> Response:
        """
        Загружает фото для объекта Pet.

        Аргументы:
            request (Request): HTTP запрос.
            pk (str, optional): Первичный ключ объекта Pet.

        Возвращает:
            Response: HTTP ответ с данными загруженного фото.
        """
        pet = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            photo = serializer.save(pet=pet)
            return Response(
                {"id": photo.id, "url": photo.get_full_url(request)},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy_photos(self, pet: Pet) -> None:
        """
        Удаляет все фото, связанные с объектом Pet.

        Аргументы:
            pet (Pet): Экземпляр модели Pet.
        """
        photos = pet.photos.all()
        for photo in photos:
            file_path = photo.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
            photo.delete()

    @action(detail=False, methods=["delete"])
    def delete(self, request) -> Response:
        """
        Удаляет объекты Pet по списку идентификаторов.

        Аргументы:
            request (Request): HTTP запрос.

        Возвращает:
            Response: HTTP ответ с информацией о результатах удаления.
        """
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count = 0
        errors = []

        for pet_id in ids:
            try:
                pet = Pet.objects.get(id=pet_id)
                with transaction.atomic():
                    self.destroy_photos(pet)
                    pet.delete()
                deleted_count += 1
            except Pet.DoesNotExist:
                errors.append(
                    {
                        "id": pet_id,
                        "error": "Pet with the matching ID was not found",
                    }
                )
            except Exception as error:
                errors.append({"id": pet_id, "error": str(error)})

        return Response(
            {"deleted": deleted_count, "errors": errors},
            status=status.HTTP_200_OK,
        )
