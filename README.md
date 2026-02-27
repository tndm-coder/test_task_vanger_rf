# Тестовое задание: Django Slider Gallery

Проект реализован на **Python 3.12 + Django 5.2** с поддержкой **MySQL** (основной вариант) и fallback на **SQLite** для быстрого локального прогона.

## Что реализовано

- Страница галереи на Bootstrap 5.
- Синхронизированный slick slider (большое изображение + превью).
- Полноэкранный просмотр по клику через GLightbox с пролистыванием.
- Админка Django с:
  - загрузкой изображений через `django-filer`;
  - drag&drop сортировкой через `django-admin-sortable2`;
  - списком с миниатюрой, названием и порядком.

## Зависимости

Все зависимости зафиксированы в `req.pip`.

## Быстрый старт (SQLite)

Подходит для локальной проверки без поднятия MySQL.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r req.pip
DB_ENGINE=django.db.backends.sqlite3 python manage.py migrate
DB_ENGINE=django.db.backends.sqlite3 python manage.py createsuperuser
DB_ENGINE=django.db.backends.sqlite3 python manage.py runserver
```

## Запуск с MySQL (основной режим)

Перед запуском задайте переменные окружения:

```bash
export DB_ENGINE=django.db.backends.mysql
export MYSQL_DATABASE=slider_db
export MYSQL_USER=slider_user
export MYSQL_PASSWORD=slider_password
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
```

Далее:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r req.pip
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Проверка результата

### 1) Админка и сортировка

1. Откройте `/admin/`.
2. Загрузите изображения в разделе **Files** (`django-filer`).
3. Создайте элементы в разделе **Элементы слайдера**.
4. На странице списка перетаскивайте строки за drag-handle — порядок должен сохраняться.

### 2) Галерея и fullscreen

1. Откройте главную страницу `/`.
2. Проверьте, что большой слайд и превью синхронизированы.
3. Кликните по большому изображению — откроется fullscreen/lightbox.
4. Переключайте изображения стрелками в fullscreen.

### 3) Базовые проверки

```bash
DB_ENGINE=django.db.backends.sqlite3 python manage.py check
DB_ENGINE=django.db.backends.sqlite3 python manage.py test
```
