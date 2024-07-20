from pets.models import Photo


class PhotoURLMixin:
    """
    Миксин для добавления метода получения полного URL файла (фотографии).
    """

    def get_url(self, obj: Photo) -> str:
        """
        Возвращает полный URL файла (фотографии).

        Аргументы:
            obj (Photo): Экземпляр модели Photo.

        Возвращает:
            str: Полный URL файла (фотографии).
        """
        request = self.context.get("request")
        return obj.get_full_url(request) if request else obj.file.url
