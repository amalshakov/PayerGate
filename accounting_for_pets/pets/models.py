import uuid

from django.db import models


class Photo(models.Model):
    """."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()

    def __str__(self) -> str:
        return self.url


class Pet(models.Model):
    """."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    type = models.CharField(max_length=50)
    photos = models.ManyToManyField(Photo)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
