# REST-Сервис получения текущей зарплаты и даты следующего повышения
## Запуск проекта на локальной машине:
1. Клонировать проект.
    ```
    git clone ...
    ```
2. Установить зависимости из requirements.txt
    ```
    pip install -r requirements.txt
    ```
   Или:
    ```
    poetry update
    ```
3. Запустить докер-контейнеры с рабочей и тестовой БД (все команды написаны из-под sudo)
    ```
    make up
    ```
4.  Создать миграции (Будут созданы таблицы в рабочей и тестовой БД)
   ```
    make migration
   ```
5. Провести миграцию (В рабочую БД будет добавлен пользователь для проверки)
   ```
    make migrate
   ```
6. Запустить проект!
    ```
    python main.py
    ```


## Запуск проекта на сервере:
1. Клонировать проект.
    ```
    git clone ...
    ```
2. Запустить докер-контейнеры с приложением и рабочей БД (все команды написаны из-под sudo)
    ```
    make run
    ```
3. Войти в докер-контейнер с приложением.
    ```
    make enter
    ```
4. Скачать текстовый редактор vim.
    ```
    apt-get update && apt-get install vim -y
    ```
5. Открыть файл alembic.ini, в который потребуется внести изменения.
Заменить значение sqlalchemy.url на:
    ```ini
    sqlalchemy.url = postgresql://postgres:postgres@db:5432/postgres
    ```
6. Провести миграции.
   ```
    make migration
   ```
### Все команды важно прописывать в рабочей дирректории
### Для просмотра зависимостей используйте: ```poetry show --tree```

## Инструкция для alembic (для дальнейшей разработки):
1. Инициализация:
```alembic init migrations```. Будет создана папка с миграциями и конфигурационный файл для alembic.
   - В alembic.ini нужно прописать адрес базы данных, в которую будут проходить миграции.
        ```ini
        sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5444/postgres # Откроет на 5444 порту.
        ```
   - В migrations/env.py нужно внести изменения. Удалить блок с импортом MyModel.
        ```python
        from myapp import mymodel
        ```
   - На его место поместить
        ```python
        from db.models import Base
        target_metadata = Base.metadata
        ```
2. Создать миграцию:
```alembic revision --autogenerate -m "comment"```

3. Запустить миграцию:
```alembic upgrade heads```
