# PayerGate
- Тестовое задание на позицию “Backend-developer” в компанию PayerGate (Python, Django, PostgreSQL, Docker)
- ТЗ - [ссылка](https://cloud.mail.ru/public/iyQB/kocLM1hPi)
- Клонируйте репозиторий
```
git clone git@github.com:amalshakov/PayerGate.git
```

- Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```

- Установите зависимости
```
pip install -r requirements.txt
```

- Запросите у разработчика файл .env и расположите его в одной директории с файлом docker-compose.yml. Либо заполните файл .env самостоятельно, ориентируясь на .env.template.

- Запустите проект. Для этого соберите образы и запустите контейнеры.
```
docker-compose build
docker-compose up
```

- Выполните миграции (создайте таблицы в БД)
```
docker-compose exec django_backend python manage.py migrate
```

- Для работы с API вам понадобится передавать "X-API-KEY" в Headers (его можно узнать в файле .env). В противном случае при запросе Вы получите: 401 Unauthorized. Либо для более удобной проверки API Вы можете отключить (закомментировать) необходимый MIDDLEWARE в [settings.py](./accounting_for_pets/accounting_for_pets/settings.py) (38 строчка)
```
    # "api.middleware.APIKeyMiddleware",
```

## Endpoints
1) http://localhost/api/v1/pets/ POST (Создать питомца)

- request body:
```
{
    "name": "palkan",
    "age": 1,
    "type": "dog"
}
```

- "type" может быть либо "dog" либо "cat".

- response body:
```
{
    "id": "70064b69-ca36-428e-9259-5b860cb59162",
    "name": "mussi",
    "age": 11,
    "type": "cat",
    "photos": [],
    "created_at": "2024-07-21T09:09:05"
}
```

2) http://localhost/api/v1/pets/{id}/photo/ POST (Загрузить фотографию питомца)
- Пример для Postman. Вкладка "Body", выбираем "form-data". В "Key" ставим: "file". В "Value" выбираем картинку. Нажимаем "Send".
- response body:
```
{
    "id": "3929a66d-f4cb-40b9-8abd-9cae356c9ac0",
    "url": "http://localhost/media/photos/20240531_123647.jpg"
}
```

3) http://localhost/api/v1/pets/ GET (Получить список питомцев)
- response body:
```
{
    "count": 5,
    "items": [
        {
            "id": "c014a026-7cbc-4860-8a4a-685769ec7d65",
            "name": "bussi",
            "age": 1,
            "type": "dog",
            "photos": [],
            "created_at": "2024-07-21T08:58:04"
        },
        {
            "id": "70064b69-ca36-428e-9259-5b860cb59162",
            "name": "mussi",
            "age": 11,
            "type": "cat",
            "photos": [],
            "created_at": "2024-07-21T09:09:05"
        },
        {
            "id": "384a24f6-0c8d-41c3-8277-02581ae546fb",
            "name": "kussi",
            "age": 5,
            "type": "cat",
            "photos": [],
            "created_at": "2024-07-21T09:11:10"
        },
        {
            "id": "3bcabbca-f657-48fa-b606-acb18b418297",
            "name": "dussi",
            "age": 5,
            "type": "cat",
            "photos": [],
            "created_at": "2024-07-21T09:11:17"
        },
        {
            "id": "5c7cfda9-75a8-4c46-bf41-bfcb11c95074",
            "name": "gussi",
            "age": 5,
            "type": "cat",
            "photos": [
                {
                    "id": "5ed64e7c-3df6-4f8f-8fe2-507eebbc2b05",
                    "url": "http://localhost/media/photos/20240531_122555.jpg"
                },
                {
                    "id": "3929a66d-f4cb-40b9-8abd-9cae356c9ac0",
                    "url": "http://localhost/media/photos/20240531_123647.jpg"
                }
            ],
            "created_at": "2024-07-21T09:11:23"
        }
    ]
}
```

- query parameters:
limit: integer (optional, default=20)
offset: integer (optional, default=0)
has_photos: boolean (optional)
has_photos: true - вернуть записи с фотографиями
has_photos: false - вернуть записи без фотографий
has_photos was not provided - вернуть все записи

- request:
http://localhost/api/v1/pets/?limit=1&offset=0&has_photos=true

- response body:
```
{
    "count": 1,
    "items": [
        {
            "id": "5c7cfda9-75a8-4c46-bf41-bfcb11c95074",
            "name": "gussi",
            "age": 5,
            "type": "cat",
            "photos": [
                {
                    "id": "5ed64e7c-3df6-4f8f-8fe2-507eebbc2b05",
                    "url": "http://localhost/media/photos/20240531_122555.jpg"
                },
                {
                    "id": "3929a66d-f4cb-40b9-8abd-9cae356c9ac0",
                    "url": "http://localhost/media/photos/20240531_123647.jpg"
                }
            ],
            "created_at": "2024-07-21T09:11:23"
        }
    ]
}
```

4) http://localhost/api/v1/pets/ DELETE (Удалить питомцев)
- response body:
```
{
    "ids": [
        "5c7cfda9-75a8-4c46-bf41-bfcb11c95074",
        "587e5358-6407-4fff-9f86-853ce1849ac7",
        "6796fa0d-f405-4363-881d-6d3694a9655c"
    ]
}
```

- response body:
```
{
    "deleted": 1,
    "errors": [
        {
            "id": "587e5358-6407-4fff-9f86-853ce1849ac7",
            "error": "Pet with the matching ID was not found"
        },
        {
            "id": "6796fa0d-f405-4363-881d-6d3694a9655c",
            "error": "Pet with the matching ID was not found"
        }
    ]
}
```

- Так же для доступа к админке, соберите статику и создайте суперюзера.
```
docker-compose exec django_backend python manage.py collectstatic
docker-compose exec django_backend python manage.py createsuperuser
```
- будет доступна админка http://localhost/admin/

### Автор:
- Александр Мальшаков (ТГ [@amalshakov](https://t.me/amalshakov), GitHub [amalshakov](https://github.com/amalshakov/))