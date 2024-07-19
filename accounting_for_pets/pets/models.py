import uuid

from django.conf import settings
from django.db import models


class Pet(models.Model):
    """."""

    CAT = "cat"
    DOG = "dog"
    PET_TYPES = [
        (CAT, "Cat"),
        (DOG, "Dog"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    type = models.CharField(max_length=50, choices=PET_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Photo(models.Model):
    """."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(
        Pet, related_name="photos", on_delete=models.CASCADE
    )
    file = models.ImageField(upload_to="photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_full_url(self, request):
        return request.build_absolute_uri(self.file.url)
