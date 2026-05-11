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
    "PASSWORD": "ваш_пароль"
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
   "PASSWORD": "ваш_пароль"
}
```

* Запустить тесты
```text
pytest -n <количество потоков> -v
```