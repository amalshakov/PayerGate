from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse


class APIKeyMiddleware:
    """Middleware для проверки API-ключа в заголовках запроса."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Обработка входящего запроса.

        Аргументы:
            request (HttpRequest): Входящий HTTP-запрос.

        Возвращает:
            HttpResponse: HTTP-ответ.

        Возвращает 401 Unauthorized, если API-ключ отсутствует или неверен.
        """
        api_key = request.headers.get("X-API-KEY")

        if not api_key or api_key != settings.API_KEY:
            return JsonResponse({"detail": "Unauthorized"}, status=401)
        return self.get_response(request)
