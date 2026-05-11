# **Финальный проект: Автотесты для сервиса Kvadra Push console**

## 1. Структура:
```text
m.tolstogyzowa_final_project/
├── fixtures/ 
│ ├── auth_fixtures.py
│ ├── project_fixtures.py
│ ├── app_fixtures.py
│ └── ui_fixtures.py
│
├── general/ 
│ ├── checkers/
│ ├── clients/ 
│ ├── helpers/ 
│ ├── route/
│ ├── requests_wrapper/
│ └── utils.py 
│
├── models/
│ ├── pydantic_models/ 
│ │ ├── app_models.py
│ │ ├── auth_models.py
│ │ ├── common_models.py
│ │ └── project_models.py
│ │
│ └── peewee_models/ 
│ └── push_console_pw_models.py
│
├── pages/
│ ├── base_page.py
│ ├── login_page.py
│ ├── projects_page.py
│ └── registry_page.py
│
├── proto_files/ 
│
├── test_data/ 
│ ├── enums.py
│ └── project_test_data.py
│
├── tests/ 
│ ├── REST/ # REST API тесты
│ │ ├── test_app.py
│ │ ├── test_auth.py
│ │ ├── test_project.py
│ │ └── test_user.py
│ │
│ ├── gRPC/ # gRPC тесты
│ │ └── test_grpc_delete_app.py
│ │
│ └── UI/ # UI тесты
│ └── selenium/
│ ├── test_selenium_app.py
│ ├── test_selenium_auth.py
│ └── test_selenium_projects.py
│
├── README.md 
├── Dockerfile
├── requirements.txt 
├── .gitignore
├── .dockerignore 
├── conftest.py
├── config.py 
├── config_file.json
├── test_cases.txt
```

## 2. Запуск через Docker 

* Склонировать репозиторий
```text
git clone <ссылка_на_репозиторий>
```

* Перейти в папку проекта
```text
cd m.tolstogyzowa_final_project
```

* Создать файл с личными данными
```text
touch config_file_local.json
```

* Внести в него свои личные данные по шаблону с помощью команды
```text 
 vim config_file_local.json
 ```
```text
 шаблон:
{
    "EMAIL": "ваша_почта@example.com",
    "PASSWORD": "ваш_пароль",
    "BASE_URL": "http://193.169.128.91/",
    "GRPC_HOST": "193.169.128.91:5000",

    "PUSH_CONSOLE_POSTGRES_HOST": "193.169.128.91",
    "PUSH_CONSOLE_POSTGRES_PORT": 10001,
    "PUSH_CONSOLE_POSTGRES_DATABASE": "postgres",
    "PUSH_CONSOLE_POSTGRES_USER": "rouser",
    "PUSH_CONSOLE_POSTGRES_PASSWORD": "Kx9mP2vL5nR8wQ4jT7yH3zB6",

    "PUSH_CONSOLE_CLICKHOUSE_HOST": "193.169.128.91",
    "PUSH_CONSOLE_CLICKHOUSE_PORT": 8123,
    "PUSH_CONSOLE_CLICKHOUSE_USER": "default",
    "PUSH_CONSOLE_CLICKHOUSE_PASSWORD": "TiEQulfQsjSh4HuXhhbPMOS+rIqF2EgLrSfQ2eClyP0=",

    "PUSH_CONSOLE_REDIS_HOST": "193.169.128.91",
    "PUSH_CONSOLE_REDIS_PORT": 10002,
    "PUSH_CONSOLE_REDIS_PASSWORD": "F2pL9kX7zQ5vN3mR",

    "PUSH_CONSOLE_RABBIT_HOST": "193.169.128.91",
    "PUSH_CONSOLE_RABBIT_PORT": 5672,
    "PUSH_CONSOLE_RABBIT_VHOST": "main_vhost",
    "PUSH_CONSOLE_RABBIT_USER": "rabbit_admin",
    "PUSH_CONSOLE_RABBIT_PASSWORD": "W4nB8yT3mK6pL9jH"
}
```

* Собрать Docker образ
```text
docker build -t my-tests-full  .
```

* Запустить тесты
```text
docker run my-tests-full pytest -n <количество потоков> -v
```

## 3. Запуск локально

* Склонировать репозиторий
```text
git clone <ссылка_на_репозиторий>
```

* Перейти в папку проекта, создать виртуальное окружение и активировать его
```text
python3 -m venv venv
```
```text
source venv/bin/activate
```

* Установить зависимости
```text
pip install -r requirements.txt
```

* Создать файл с личными данными config_file_local.json по шаблону
```text
{
    "EMAIL": "ваша_почта@example.com",
    "PASSWORD": "ваш_пароль",
    "BASE_URL": "http://193.169.128.91/",
    "GRPC_HOST": "193.169.128.91:5000",

    "PUSH_CONSOLE_POSTGRES_HOST": "193.169.128.91",
    "PUSH_CONSOLE_POSTGRES_PORT": 10001,
    "PUSH_CONSOLE_POSTGRES_DATABASE": "postgres",
    "PUSH_CONSOLE_POSTGRES_USER": "rouser",
    "PUSH_CONSOLE_POSTGRES_PASSWORD": "Kx9mP2vL5nR8wQ4jT7yH3zB6",

    "PUSH_CONSOLE_CLICKHOUSE_HOST": "193.169.128.91",
    "PUSH_CONSOLE_CLICKHOUSE_PORT": 8123,
    "PUSH_CONSOLE_CLICKHOUSE_USER": "default",
    "PUSH_CONSOLE_CLICKHOUSE_PASSWORD": "TiEQulfQsjSh4HuXhhbPMOS+rIqF2EgLrSfQ2eClyP0=",

    "PUSH_CONSOLE_REDIS_HOST": "193.169.128.91",
    "PUSH_CONSOLE_REDIS_PORT": 10002,
    "PUSH_CONSOLE_REDIS_PASSWORD": "F2pL9kX7zQ5vN3mR",

    "PUSH_CONSOLE_RABBIT_HOST": "193.169.128.91",
    "PUSH_CONSOLE_RABBIT_PORT": 5672,
    "PUSH_CONSOLE_RABBIT_VHOST": "main_vhost",
    "PUSH_CONSOLE_RABBIT_USER": "rabbit_admin",
    "PUSH_CONSOLE_RABBIT_PASSWORD": "W4nB8yT3mK6pL9jH"
}
```

* Запустить тесты
```text
pytest -n <количество потоков> -v
```