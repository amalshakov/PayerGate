from rest_framework import serializers

from pets.models import Pet, Photo


class PhotoSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Photo
        fields = ["id", "url"]


class PetSerializer(serializers.ModelSerializer):
    """."""

    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "age", "type", "photos", "created_at"]


class PetCreateSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Pet
        fields = ["id", "name", "age", "type"]

    def create(self, validated_data):
        return Pet.objects.create(**validated_data)
