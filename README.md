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


## Быстрый старт (Windows PowerShell + SQLite)

Если проверка идёт на Windows, используйте PowerShell-команды:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r req.pip
$env:DB_ENGINE="django.db.backends.sqlite3"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Smoke/autotests в PowerShell:

```powershell
$env:DB_ENGINE="django.db.backends.sqlite3"
python manage.py check
python manage.py test
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


## Небольшой план тестирования (этап 5)

Упор делаем на автотесты, без разворачивания большой QA-документации.

### Приоритет 1 — backend автотесты (обязательно)

1. **Модель `SliderItem`**
   - проверка русских `verbose_name`/`verbose_name_plural`;
   - проверка `ordering`;
   - проверка `__str__`.
2. **Админка `SliderItemAdmin`**
   - проверка конфигурации списка (`list_display`, `list_display_links`, `ordering`);
   - проверка рендера миниатюры и fallback, если изображения нет.
3. **Представление `slider_page`**
   - пустое состояние (сообщение «Слайды пока не добавлены»);
   - корректная выборка с `select_related(...).order_by(...)`;
   - корректная передача слайдов в HTML (title, image URL, индексы для fullscreen).

### Приоритет 2 — smoke checks (обязательно)

- `python manage.py check`
- `python manage.py test`

### Приоритет 3 — ручная проверка (коротко)

- 5–10 минут на проверку в браузере:
  - drag&drop порядка в админке;
  - синхронизация main/nav в слайдере;
  - открытие и листание в fullscreen.
