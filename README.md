#  API системы опросов пользователей.

<p align="left">
<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://pycqa.github.io/isortE"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>


![Screenshot](cover.png)

## Задача
Спроектировать и разработать API для системы опросов пользователей.

#### Функционал для администратора системы:
- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

#### Функционал для пользователей системы:
- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

#### Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API


## Техническое описание
* Реализован на базе RestAPI.
* Технология - Django Rest Framework
* Документация по ресурсам на http://127.0.0.1:8000/api/v1/swagger/

## Установка
Устанавливаем docker и docker-compose:
```
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
usermod -aG docker $USER
```

Устанавливаем Pipenv:
```
pip3 install pipenv
```

Копируем проект:
```
git clone https://github.com/AlexKhlybov/drf_polls.git
```

Переходим в папку проекта:
```
cd drf_polls
```

Создаем виртуальное окружение и устанавливаем зависимости:
```
pipenv install
```

Активируем виртуальное окружение:
```
pipenv shell
```

Копируем пример файла .env, после копирования, загляните в него, может быть вы захотите внести свои секреты:
```
cp example.env .env
```

Поднимаем базу данных в докер
```
docker-compose up -d
```

Создаем и накатываем миграции:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Создаем админа, фдминка доступна по адресу - http://127.0.0.1:8000/admin:
```
python3 manage.py createsuperuser
```

Запускаем сервер:
```
python3 manage.py runserver
```

## Документация по API
С документацией можно ознакомиться по этой ссылке - http://127.0.0.1:8000/api/v1/swagger/


## Лицензия
MIT
