import re
import uuid
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpRequest


class Pet(models.Model):
    """Модель, представляющая питомца."""

    CAT = "cat"
    DOG = "dog"
    PET_TYPES = [
        (CAT, "Cat"),
        (DOG, "Dog"),
    ]

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name: str = models.CharField(max_length=100)
    age: int = models.IntegerField()
    type: str = models.CharField(max_length=50, choices=PET_TYPES)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def clean_fields(self, exclude: Optional[list[str]] = None) -> None:
        """
        Проверяет поля модели на корректность.

        Аргументы:
            exclude (Optional[list[str]]): Список имен полей,
            которые нужно исключить из проверки.

        Исключения:
            ValidationError: Если возраст выходит за пределы 0-30
            или имя содержит неалфавитные символы.
        """
        super().clean_fields(exclude=exclude)
        if self.age < 0 or self.age > 30:
            raise ValidationError(
                {"age": "Возраст должен быть от 0 до 30 включительно."}
            )
        if not re.match(r"^[A-Za-z]+$", self.name):
            raise ValidationError(
                {"name": "Имя должно содержать только буквы."}
            )

    def __str__(self) -> str:
        return self.name


class Photo(models.Model):
    """Модель, представляющая фотографию питомца."""

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    pet: Pet = models.ForeignKey(
        Pet, related_name="photos", on_delete=models.CASCADE
    )
    file: models.ImageField = models.ImageField(upload_to="photos/")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def get_full_url(self, request: HttpRequest) -> str:
        """Получает полный URL файла фотографии."""
        return request.build_absolute_uri(self.file.url)
