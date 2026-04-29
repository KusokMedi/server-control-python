# WebControl - Система удаленного управления компьютером

> **[Read this in English](README_EN.md)**

Безопасная система удаленного управления компьютером через веб-интерфейс с поддержкой множественных пользователей, ролей и аудита действий.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 📋 Содержание

- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Установка](#установка)
- [Использование](#использование)
- [API](#api)
- [Конфигурация](#конфигурация)
- [Безопасность](#безопасность)
- [Структура проекта](#структура-проекта)
- [Разработка](#разработка)
- [Лицензия](#лицензия)

## ✨ Возможности

### 🔐 Безопасность
- Хеширование паролей (Werkzeug)
- Rate limiting (защита от брутфорса)
- CSRF защита на всех формах
- Защита от SQL инъекций (SQLAlchemy ORM)
- Audit trail - полное логирование действий

### 👥 Управление пользователями
- Создание, редактирование, удаление пользователей
- Система ролей: **admin** и **user**
- Активация/деактивация пользователей
- Смена паролей и настроек

### 🌍 Мультиязычность
- Русский язык (по умолчанию)
- Английский язык
- Выбор языка для каждого пользователя
- Легко добавить новые языки

### 📊 Мониторинг системы
- CPU, RAM, Disk, Network в реальном времени
- Графики использования ресурсов
- Локальный и внешний IP

### 🖥️ Управление процессами
- Просмотр всех процессов
- Завершение процессов
- Изменение приоритета
- Поиск и сортировка

### 🪟 Управление окнами
- Список всех окон
- Скрытие/показ окон
- Перемещение и изменение размера
- Закрытие окон

### ⌨️ Эмуляция ввода
- Управление мышью (перемещение, клики, прокрутка)
- Управление клавиатурой (ввод текста, нажатие клавиш)
- Получение позиции мыши

### 📸 Скриншоты
- Захват текущего монитора
- Захват всех мониторов
- Захват выбранного монитора
- Отображение курсора на скриншоте

### 📋 Буфер обмена
- Чтение содержимого
- Запись текста
- Очистка

### 🎥 Стриминг экрана
- Просмотр экрана в реальном времени
- Выбор монитора
- Настройка качества

### 📝 Логирование
- Структурированные логи (app.log, error.log)
- Ротация логов (10MB, 10 файлов)
- Audit logs в базе данных
- Просмотр и скачивание логов (только admin)

## 🚀 Быстрый старт

### Windows

```cmd
REM 1. Установить зависимости
install.bat

REM 2. Инициализировать БД
flask init-db

REM 3. Создать администратора
flask create-admin

REM 4. Запустить приложение
start.bat
```

### Linux

```bash
# 1. Установить зависимости
./install.sh

# 2. Инициализировать БД
flask init-db

# 3. Создать администратора
flask create-admin

# 4. Запустить приложение
./start.sh
```

Откройте браузер: **http://localhost:5000**

## 📦 Установка

### Требования

- Python 3.8+
- Windows или Linux
- Права администратора (для некоторых функций)

**Примечание:** Управление окнами доступно только на Windows. Все остальные функции работают на обеих платформах.

### Шаг 1: Клонирование репозитория

```bash
git clone <repository-url>
cd server-control-python
```

### Шаг 2: Установка зависимостей

**Windows:**
```cmd
install.bat
```

**Linux:**
```bash
chmod +x install.sh start.sh clear.sh
./install.sh
```

### Шаг 3: Запуск приложения

```bash
python main.py
```

Откройте браузер: **http://localhost:5000**

При первом запуске вы увидите страницу настройки, где нужно создать первого администратора.

### Шаг 4: Создание администратора

На странице настройки введите:
- Имя пользователя (минимум 3 символа)
- Пароль (минимум 6 символов)
- Подтверждение пароля
- Выберите язык интерфейса

После создания администратора вы будете перенаправлены на страницу входа.

## 💻 Использование

### Запуск приложения

**Режим разработки:**
```bash
python main.py
```

**Режим production (Windows):**
```cmd
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 main:app
```

**Режим production (Linux):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### CLI Команды

```bash
# Инициализация БД
flask init-db

# Создать администратора
flask create-admin

# Список пользователей
flask list-users
```

### Очистка данных

Удаляет базу данных, логи и скриншоты:

**Windows:**
```cmd
clear.bat
```

**Linux:**
```bash
./clear.sh
```

## 🔌 API

Все API endpoints требуют аутентификации. Некоторые требуют роль администратора.

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/login` | Вход в систему |
| GET | `/logout` | Выход из системы |

### Пользователи (только admin)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/users` | Список пользователей |
| POST | `/api/users` | Создать пользователя |
| PUT | `/api/users/<id>` | Обновить пользователя |
| DELETE | `/api/users/<id>` | Удалить пользователя |
| GET | `/api/users/me` | Текущий пользователь |

**Пример создания пользователя:**
```json
POST /api/users
{
  "username": "user1",
  "password": "password123",
  "role": "user",
  "language": "ru"
}
```

### Процессы

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/processes` | Список процессов |
| POST | `/api/processes/kill` | Завершить процесс |
| POST | `/api/processes/priority` | Изменить приоритет |

### Мониторинг

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/monitoring` | Статистика системы |

### Окна

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/windows` | Список окон |
| POST | `/api/windows/hide` | Скрыть окно |
| POST | `/api/windows/show` | Показать окно |
| POST | `/api/windows/minimize` | Свернуть окно |
| POST | `/api/windows/maximize` | Развернуть окно |
| POST | `/api/windows/close` | Закрыть окно |
| POST | `/api/windows/move` | Переместить окно |
| POST | `/api/windows/focus` | Активировать окно |

### Ввод

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/input/mouse/position` | Позиция мыши |
| POST | `/api/input/mouse/move` | Переместить мышь |
| POST | `/api/input/mouse/click` | Клик мыши |
| POST | `/api/input/mouse/scroll` | Прокрутка |
| POST | `/api/input/keyboard/type` | Ввод текста |
| POST | `/api/input/keyboard/press` | Нажатие клавиши |

### Скриншоты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/monitors` | Список мониторов |
| POST | `/api/screenshot` | Сделать скриншот |

**Пример запроса скриншота:**
```json
POST /api/screenshot
{
  "mode": "current",
  "show_cursor": true,
  "cursor_style": "crosshair"
}
```

### Буфер обмена

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/clipboard/read` | Прочитать |
| POST | `/api/clipboard/write` | Записать |
| POST | `/api/clipboard/clear` | Очистить |

### Логи (только admin)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/logs` | Логи приложения |
| GET | `/api/logs/audit` | Аудит действий |
| GET | `/api/logs/download` | Скачать логи |
| POST | `/api/logs/clear` | Очистить логи |

### Стриминг

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/monitors` | Список мониторов |
| POST | `/api/stream` | Получить кадр |

## ⚙️ Конфигурация

### Переменные окружения (.env)

```env
# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# Server
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_URL=sqlite:///webcontrol.db

# Security
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://
RATELIMIT_ENABLED=True
```

### Добавление нового языка

1. Создайте файл `translations/xx.yml` (где xx - код языка)
2. Скопируйте структуру из `ru.yml` или `en.yml`
3. Переведите все строки
4. Добавьте язык в валидацию в `api/users.py`

## 🔒 Безопасность

### Реализованные меры

- ✅ Хеширование паролей (Werkzeug)
- ✅ Rate limiting (5 попыток входа/минуту)
- ✅ CSRF защита на всех формах
- ✅ SQL инъекции невозможны (SQLAlchemy ORM)
- ✅ HttpOnly cookies
- ✅ Безопасное логирование (без паролей)
- ✅ Audit trail в БД

### Рекомендации

1. **Используйте сильный SECRET_KEY** - сгенерируйте случайный ключ
2. **HTTPS** - используйте HTTPS в production
3. **Firewall** - ограничьте доступ к порту
4. **Сильные пароли** - требуйте сложные пароли
5. **Регулярные обновления** - обновляйте зависимости
6. **Аудит** - проверяйте логи

### Rate Limiting

- Логин: **5 попыток в минуту**
- API: **200 запросов в день, 50 в час**

## 📁 Структура проекта

```
server-control-python/
├── api/                    # API endpoints
│   ├── clipboard.py
│   ├── control.py
│   ├── input.py
│   ├── logs.py
│   ├── monitoring.py
│   ├── processes.py
│   ├── screenshots.py
│   ├── users.py
│   └── windows.py
├── static/                 # Статические файлы
│   ├── css/
│   ├── js/
│   ├── images/
│   └── screenshots/
├── templates/              # HTML шаблоны
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── 404.html
├── translations/           # Переводы
│   ├── ru.yml
│   └── en.yml
├── utils/                  # Утилиты и модули
│   ├── api_utils.py
│   ├── auth.py
│   ├── cli.py
│   ├── config.py
│   ├── i18n.py
│   ├── logger.py
│   ├── models.py
│   └── system_utils.py
├── logs/                   # Логи
├── main.py                 # Главный файл
├── run.py                  # Альтернативный запуск
├── requirements.txt        # Зависимости
├── .env.example            # Пример конфигурации
├── install.bat / .sh       # Установка
├── start.bat / .sh         # Запуск
├── clear.bat / .sh         # Очистка данных
└── README.md
```

## 🛠️ Разработка

### Добавление нового API endpoint

1. Создайте функцию в соответствующем файле в `api/`
2. Добавьте декораторы `@require_auth` или `@require_role('admin')`
3. Используйте `@handle_errors` для обработки ошибок
4. Добавьте `log_audit()` для важных действий

**Пример:**
```python
@my_bp.route('/my-endpoint', methods=['POST'])
@require_auth
@handle_errors
def my_endpoint():
    data = request.get_json()
    # Ваш код
    log_audit('my_action', 'Description')
    return jsonify({'success': True})
```

### Добавление новой модели

1. Добавьте класс в `utils/models.py`
2. Запустите `flask init-db` для создания таблиц

### Тестирование

```bash
# Запуск в режиме разработки
export FLASK_DEBUG=True
python main.py
```

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🤝 Поддержка

Для вопросов и предложений создайте issue в репозитории.

---

**WebControl** - Полный контроль над вашим компьютером через браузер 🚀
