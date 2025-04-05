# Astrology Bot Project

Проект представляет собой систему из трех микросервисов: Telegram-бота для получения гороскопов, REST API сервиса гороскопов и PostgreSQL базы данных.

## Состав проекта

1. **Telegram Bot** - предоставляет интерфейс для пользователей
2. **Horoscope API** - REST API сервис для работы с гороскопами
3. **PostgreSQL** - база данных для хранения информации

## Требования

- Docker (версия 20.10.0 или выше)
- Docker Compose (версия 1.29.0 или выше)

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Juonior/astrology_bot.git
   cd astrology_bot
   ```

2. Создайте Docker network (если еще не создана):
   ```bash
   docker network create horoscope
   ```

3. Запустите сервисы с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Сервисы будут доступны:
   - Бот: в Telegram по указанному токену
   - API: http://localhost:8000
   - PostgreSQL: localhost:5436

## Конфигурация

Основные настройки задаются через переменные окружения в `docker-compose.yml`:

### Telegram Bot
- `BOT_TOKEN` - токен вашего Telegram бота
- `POSTGRES_*` - параметры подключения к БД
- `HOROSCOPE_API_BASE_URL` - URL API сервиса

### Horoscope API
- `APP_HOST` - хост для запуска API
- `APP_PORT` - порт для запуска API
- `DEBUG` - режим отладки (True/False)

### PostgreSQL
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь БД
- `POSTGRES_PASSWORD` - пароль пользователя

## Команды управления

- Запуск всех сервисов:
  ```bash
  docker-compose up -d
  ```

- Остановка всех сервисов:
  ```bash
  docker-compose down
  ```

- Просмотр логов бота:
  ```bash
  docker logs -f astrology_bot
  ```

- Просмотр логов API:
  ```bash
  docker logs -f horoscope-api
  ```

- Проверка состояния БД:
  ```bash
  docker exec -it telegram_bot_postgres psql -U bot_user -d telegram_bot_db
  ```

## Особенности работы

1. База данных инициализируется скриптом `init.sql` при первом запуске
2. Все сервисы перезапускаются автоматически при падении (unless-stopped)
3. Для БД настроен healthcheck для проверки готовности
4. Логи бота сохраняются в директорию `telegram-bot/logs`
