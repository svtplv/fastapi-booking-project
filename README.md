# fastapi-booking-project
## Описание:

Сервис бронирования отелей. На данный момент готовы: 

* Регистрация и аутентификация пользователя через JWT токен
* Получение списка доступных для заселения отелей
* Получение списка номеров в определенном отеле
* Бронь номера на определенный промежуток времени
* Отмена брони 
* Загрузка изображений отелей
* Кеширование с помощью Redis
* Фоновая обработка картинок 
* Фоновая отправка сообщения на почту

### Стек технологий:
* Python 3.10
* FastAPI
* PostgreSQL
* SQLAlchemy
* PostgreSQL
* Redis
* Celery
* Pytest

### Установка:

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:svtplv/fastapi-booking-project.git
```

2. Cоздать и активировать виртуальное окружение:
* Linux/macOS:
```
python3 -m venv venv
source venv/bin/activate
```
* Windows:
```
python -m venv venv
source env/scripts/activate
```

3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

4. Создать .env файл в корне по образцу .env example.

5. Выполнить миграции:
```
alembic upgrade head
```

6. Наполнить данными, выполнив запросы из файла test_data_db.sql

7. Запустить redis
```
redis-server.exe
```

8. Запустить celery
``` 
celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo
```

9. Запустить celery flower
``` 
celery -A app.tasks.tasks:celery flower
```

10. Запустить проект:
``` 
uvicorn app.main:app
```

### Авторы:
[Святослав Поляков](https://github.com/svtplv)
