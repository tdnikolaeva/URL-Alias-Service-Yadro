# URL Alias Service

Cервис преобразования длинных URL в короткие уникальные URL. Сервис представляет из себя REST API, и осуществляет создание таких URL, их менеджмент, а также перенаправление на оригинальный ресурс при обращении к коротким URL, и сбор статистики по переходам.

# Добавление пользователей??????????????????

Создание пользователей/паролей встроено в используемый фреймворк Django (DRF). Для этого используется команда:

```bash
python mange.py createsuperuser
```



# Инструкция по запуску

#### 1 - Склонируйте репозиторий
```bash
git clone https://github.com/tdnikolaeva/URL-Alias-Service-Yadro.git
```

#### 2 - Перейдите в папку проекта
```bash
cd URL-Alias-Service-Yadro
```

#### 3 - Активируйте виртуальное окружение и установите зависимости
```bash
python -m venv venv
source venv/bin/scripts/activate #линукс
venv/scripts/activate #винда

pip install -r requirements.txt
```

#### 4 - Создайте в корне проекта `.env` файл 

Его наполнение должно содержать:

```
SECRET_KEY=ejxv#nkwq$8)06$6b^2r=ejxv#nkwq$8)06$6b^2r=+fz8sa=gdg*j^$3m2i5om56l@ks!h
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Если вы не укажете какие-то переменные или не создадите файл, будут применены дефолтные значения.

#### 5 - Перейдите в папку с реализованным API
```bash
cd urlalias
```

#### 6 - Примените миграции
```bash
python manage.py migrate
```

#### 7 - Создайте пользователя????????????????

С помощью введенных данных возможно будет производить Basic аутентификацию.

```bash
python manage.py createsuperuser
```

#### 8 - Запустите сервер
```bash
python manage.py runserver
```

Swagger документация доступна по адресу `http://localhost:8000/docs/`
