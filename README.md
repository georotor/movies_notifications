# Проектная работа 10 спринта

[![CI](https://github.com/georotor/notifications_sprint_1/actions/workflows/code_style.yml/badge.svg)](https://github.com/georotor/notifications_sprint_1/actions/workflows/code_style.yml)

https://github.com/georotor/notifications_sprint_1

## Сервис уведомлений

Реализованные возможности:
- Отправка уведомленй по запросу в API
- Планирование отправки уведомлений как по времени, так и периодически повторяемых
- Управление шаблонами для уведомлений

## Архитектура
![Архитектура](https://github.com/georotor/notifications_sprint_1/blob/main/docs/schema.png?raw=true)

## Компоненты сервиса
- [API управления рассылками и шаблонами](https://github.com/georotor/notifications_sprint_1/tree/main/api)
- [Планировщик рассылки уведомлений](https://github.com/georotor/notifications_sprint_1/tree/main/scheduler)
- [Воркер отправки уведомлений](https://github.com/georotor/notifications_sprint_1/tree/main/worker)

## Запуск сервиса

Запуск осуществляется коммандой: `docker-compose up --build`

После старта будет доступен [Swagger API](http://127.0.0.1/api/openapi).

Планировщик и воркер так же полнимутся, но надо учитывать что для их корректной работы необходим рабочий Auth сервис, т.к. запрашивают в нем данные о получателях.
