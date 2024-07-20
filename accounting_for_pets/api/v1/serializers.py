import re

from django.conf import settings
from rest_framework import serializers

from api.v1.mixins import PhotoURLMixin
from pets.models import Pet, Photo


class PhotoSerializer(serializers.ModelSerializer, PhotoURLMixin):
    """
    Сериализатор для модели Photo, включающий URL для фотографии.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "url"]


class PetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Pet, включающий связанные фотографии.
    """

    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "age", "type", "photos", "created_at"]

    def validate_age(self, value: int) -> int:
        """
        Проверка, что возраст находится в допустимых пределах.

        Аргументы:
            value (int): Возраст питомца.

        Возвращает:
            int: Возраст, если он находится в пределах от
            settings.PET_AGE_MIN до settings.PET_AGE_MAX включительно.

        Вызывает:
            serializers.ValidationError: Если возраст не в допустимых пределах.
        """
        if value < settings.PET_AGE_MIN or value > settings.PET_AGE_MAX:
            raise serializers.ValidationError(
                {
                    "age": (
                        "Возраст питомца должен быть от "
                        f"{settings.PET_AGE_MIN} до "
                        f"{settings.PET_AGE_MAX} включительно."
                    )
                }
            )
        return value

    def validate_name(self, value: str) -> str:
        """
        Проверка, что имя содержит только буквы.

        Аргументы:
            value (str): Имя питомца.

        Возвращает:
            str: Имя, если оно содержит только буквы.

        Вызывает:
            serializers.ValidationError: Если имя содержит не только буквы.
        """
        if not re.match(settings.VALID_NAME_REGEX, value):
            raise serializers.ValidationError(
                "Имя питомца должно содержать только буквы."
            )
        return value


class PhotoUploadSerializer(serializers.ModelSerializer, PhotoURLMixin):
    """Сериализатор для загрузки фото, включающий URL для фото."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "file", "url"]

    def create(self, validated_data: dict) -> Photo:
        """
        Создает новый экземпляр модели Photo.

        Аргументы:
            validated_data (dict): Проверенные данные для создания фото.

        Возвращает:
            Photo: Новый экземпляр модели Photo.
        """
        return Photo.objects.create(**validated_data)
