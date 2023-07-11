# Movies: Сервис уведомлений

[![CI](https://github.com/georotor/movies_notifications/actions/workflows/tests.yml/badge.svg)](https://github.com/georotor/movies_notifications/actions/workflows/tests.yml)
[![CI](https://github.com/georotor/movies_notifications/actions/workflows/code_style.yml/badge.svg)](https://github.com/georotor/movies_notifications/actions/workflows/code_style.yml)

## Архитектура
![Архитектура](https://github.com/georotor/movies_notifications/blob/main/docs/schema.png?raw=true)

## Реализованные возможности
- Отправка уведомлений по запросу в API
- Планирование отправки уведомлений как по времени, так и периодически повторяемых
- Управление шаблонами для уведомлений

## Описание компонентов сервиса
- [API управления рассылками и шаблонами](https://github.com/georotor/movies_notifications/tree/main/api)
- [Планировщик рассылки уведомлений](https://github.com/georotor/movies_notifications/tree/main/scheduler)
- [Воркер отправки уведомлений](https://github.com/georotor/movies_notifications/tree/main/worker)

## Запуск сервиса

Для запуска потребуется 3 файла с переменными окружения:

- `.env.api` с настройками для API: 
  - `cp .env.api.example .env.api`
- `.env.scheduler` с настройками для планировщика: 
  - `cp .env.scheduler.example .env.scheduler`
- `.env.worker` с настройками для воркера: 
  - `cp .env.worker.example .env.worker`

Запуск осуществляется командой: `docker-compose up --build`

После старта будет доступен [Swagger API](http://127.0.0.1/api/openapi).

Планировщик и воркер так же поднимутся, но надо учитывать что для их корректной работы необходим рабочий Auth сервис, т.к. запрашивают в нем данные о получателях.

## Тестирование
```
docker-compose -f api/src/tests/functional/docker-compose.yml up --build tests
```
