from pets.models import Photo


class PhotoURLMixin:
    """
    Миксин для добавления метода получения полного URL файла фото.
    """

    def get_url(self, obj: Photo) -> str:
        """
        Возвращает полный URL файла фото.

        Аргументы:
            obj (Photo): Экземпляр модели Photo.

        Возвращает:
            str: Полный URL файла фото.
        """
        request = self.context.get("request")
        return obj.get_full_url(request) if request else obj.file.url
