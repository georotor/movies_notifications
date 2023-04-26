# API для управления рассылками

API разделено на группы.

### Schedulers

---
CRUD для управления запланированными и регулярными рассылками.
Уведомления доставляются с учетом часового пояса, это надо учитывать при планировании,
т.к. возможны ситуации когда выбранное время для доставки уведомления у пользователя уже прошло,
в этом случае сообщение **не будет доставлено**.


```json
{
  "scheduled_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "string",
  "timestamp_start": 1999999,
  "cron": "*/10 * * * *",
  "type": "email",
  "template_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "users": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "data": {},
  "enabled": true
}
```

Одно из полей: `timestamp_start` или `cron`, обязательно.


`scheduled_id` - индифиактор, при создании назначается автоматически

`name` - название, для удобства управления

`timestamp_start` - время в секундах, используется для разовых рассылок, 
у этого поля приоритет над `cron`, если указаны оба, рассылка выполнится по `timestamp_start` 

`cron` - стандартное cron выражение `0 12 */30 * *` для повторяемых уведомлений,
так же как `timestamp_start` учитывает временную зону получателя

`type` - тип уведомления, доступно только `email`

`template_id` - индификатор используемого шаблона для рассылки 

`users` - список пользователей, которым предназначается уведомление

`data` - дополнительные данные, которыми может обогащаться шаблон рассылки

`enabled` - bool, для управления рассылкой

Остальное описание доступно в Swagger после запуска.

### Notifications

---
Предназначено для создания немедленных отправок по событию.
```json
{
  "template_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "event": "registered",
  "type": "email",
  "users": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "data": {}
}
```
Одно из полей: `template_id` или `event`, обязательно. По ним ищется шаблон, для оформления уведомления.

`template_id` - индификатор шаблона

`event` - событие, на данный момент поддерживается только `registered`

`type` - тип уведомления, доступно только `email`

`users` - список пользователей, которым предназначается уведомление

`data` - дополнительные данные, которыми может обогащаться шаблон рассылки


### Templates

---
CRUD для управления шаблонами уведомлений.
Т.к. он стандартный, описание доступно в Swagger после запуска.

