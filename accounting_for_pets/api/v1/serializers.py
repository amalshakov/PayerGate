import re

from rest_framework import serializers

from pets.models import Pet, Photo


class PhotoSerializer(serializers.ModelSerializer):
    """."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "url"]

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_full_url(request) if request else obj.file.url


class PetSerializer(serializers.ModelSerializer):
    """."""

    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "age", "type", "photos", "created_at"]

    def validate_age(self, value):
        if value < 0 or value > 30:
            raise serializers.ValidationError(
                "Age must be between 0 and 30 inclusive."
            )
        return value

    def validate_name(self, value):
        if not re.match(r"^[A-Za-z]+$", value):
            raise serializers.ValidationError(
                "Name must contain only letters."
            )
        return value

    # def validate_type(self, value):
    #     if value not in ["cat", "dog"]:
    #         raise serializers.ValidationError(
    #             "Type must be either 'cat' or 'dog'"
    #         )
    #     return value


# class PetCreateSerializer(serializers.ModelSerializer):
#     """."""

#     class Meta:
#         model = Pet
#         fields = ["id", "name", "age", "type"]

#     def create(self, validated_data):
#         return Pet.objects.create(**validated_data)


class PhotoUploadSerializer(serializers.ModelSerializer):
    """."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "file", "url"]

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_full_url(request) if request else obj.file.url

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)
