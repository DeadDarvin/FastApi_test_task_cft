# REST-Сервис получения текущей зарплаты и даты следующего повышения
## Запуск проекта на локальной машине:
1. Клонировать проект.
    ```
    git clone https://gitlab.com/darvin_fastapi/test_task_for_cft.git
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
4. Создать миграции (Будут созданы таблицы в рабочей и тестовой БД)
    ```
    make migration
    ```
5. Провести миграцию (В рабочую БД будет добавлен пользователь для проверки.
username: chetkypacan@yandex.ru, password: 12345)
    ```
    make migrate
    ```
6. Запустить тесты
    ```
    pytest
    ```
7. Запустить проект!
    ```
    python main.py
    ```


## Запуск проекта на сервере:
1. Клонировать проект.
    ```
    git clone https://gitlab.com/darvin_fastapi/test_task_for_cft.git
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
6. Создать миграции.
   ```
    make migration
   ```
### Все команды важно прописывать в рабочей директории
### Для просмотра зависимостей используйте: ```poetry show --tree```:
```commandline
alembic 1.11.1 A database migration tool for SQLAlchemy.
├── mako *
│   └── markupsafe >=0.9.2
├── sqlalchemy >=1.3.0
│   └── greenlet !=0.4.17
└── typing-extensions >=4
asyncpg 0.27.0 An asyncio PostgreSQL driver
bcrypt 4.0.1 Modern password hashing for your software and your servers
envparse 0.2.0 Simple environment variable parsing
fastapi 0.88.0 FastAPI framework, high performance, easy to learn, fast to code, ready for production
├── pydantic >=1.6.2,<1.7 || >1.7,<1.7.1 || >1.7.1,<1.7.2 || >1.7.2,<1.7.3 || >1.7.3,<1.8 || >1.8,<1.8.1 || >1.8.1,<2.0.0
│   ├── email-validator >=1.0.3
│   │   ├── dnspython >=2.0.0
│   │   └── idna >=2.0.0
│   └── typing-extensions >=4.2.0
└── starlette 0.22.0
    ├── anyio >=3.4.0,<5
    │   ├── exceptiongroup *
    │   ├── idna >=2.8
    │   └── sniffio >=1.1
    └── typing-extensions >=3.10.0
greenlet 2.0.2 Lightweight in-process concurrent programming
httpx 0.23.3 The next generation HTTP client.
├── certifi *
├── httpcore >=0.15.0,<0.17.0
│   ├── anyio >=3.0,<5.0
│   │   ├── exceptiongroup *
│   │   ├── idna >=2.8
│   │   └── sniffio >=1.1
│   ├── certifi *
│   ├── h11 >=0.13,<0.15
│   └── sniffio ==1.* (circular dependency aborted here)
├── rfc3986 >=1.3,<2
│   └── idna *
└── sniffio *
passlib 1.7.4 comprehensive password hashing framework supporting over 30 schemes
pre-commit 2.21.0 A framework for managing and maintaining multi-language pre-commit hooks.
├── cfgv >=2.0.0
├── identify >=1.0.0
├── nodeenv >=0.11.1
│   └── setuptools *
├── pyyaml >=5.1
└── virtualenv >=20.10.0
    ├── distlib >=0.3.6,<1
    ├── filelock >=3.11,<4
    └── platformdirs >=3.2,<4
psycopg2-binary 2.9.6 psycopg2 - Python-PostgreSQL Database Adapter
pydantic 1.10.9 Data validation and settings management using python type hints
├── email-validator >=1.0.3
│   ├── dnspython >=2.0.0
│   └── idna >=2.0.0
└── typing-extensions >=4.2.0
pytest 7.3.1 pytest: simple powerful testing with Python
├── colorama *
├── exceptiongroup >=1.0.0rc8
├── iniconfig *
├── packaging *
├── pluggy >=0.12,<2.0
└── tomli >=1.0.0
pytest-asyncio 0.20.3 Pytest support for asyncio
└── pytest >=6.1.0
    ├── colorama *
    ├── exceptiongroup >=1.0.0rc8
    ├── iniconfig *
    ├── packaging *
    ├── pluggy >=0.12,<2.0
    └── tomli >=1.0.0
python-jose 3.3.0 JOSE implementation in Python
├── ecdsa !=0.15
│   └── six >=1.9.0
├── pyasn1 *
└── rsa *
    └── pyasn1 >=0.1.3
python-multipart 0.0.5 A streaming multipart parser for Python
└── six >=1.4.0
sentry-sdk 1.25.1 Python client for Sentry (https://sentry.io)
├── certifi *
├── fastapi >=0.79.0
│   ├── pydantic >=1.6.2,<1.7 || >1.7,<1.7.1 || >1.7.1,<1.7.2 || >1.7.2,<1.7.3 || >1.7.3,<1.8 || >1.8,<1.8.1 || >1.8.1,<2.0.0
│   │   ├── email-validator >=1.0.3
│   │   │   ├── dnspython >=2.0.0
│   │   │   └── idna >=2.0.0
│   │   └── typing-extensions >=4.2.0
│   └── starlette 0.22.0
│       ├── anyio >=3.4.0,<5
│       │   ├── exceptiongroup *
│       │   ├── idna >=2.8 (circular dependency aborted here)
│       │   └── sniffio >=1.1
│       └── typing-extensions >=3.10.0 (circular dependency aborted here)
└── urllib3 >=1.26.11
sqlalchemy 1.4.48 Database Abstraction Library
└── greenlet !=0.4.17
starlette-exporter 0.15.1 Prometheus metrics exporter for Starlette applications.
├── prometheus-client >=0.12
└── starlette *
    ├── anyio >=3.4.0,<5
    │   ├── exceptiongroup *
    │   ├── idna >=2.8
    │   └── sniffio >=1.1
    └── typing-extensions >=3.10.0
uvicorn 0.20.0 The lightning-fast ASGI server.
├── click >=7.0
│   └── colorama *
└── h11 >=0.8

```

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
