db.notifications.createIndex({ notification_id: 1 }, { unique: true });
db.scheduled_notifications.createIndex({ scheduled_id: 1 }, { unique: true });
db.templates.createIndex({ template_id: 1 }, { unique: true });

db.templates.insertOne({
  template_id: UUID(),
  name: 'Регистрация нового пользователя',
  event: 'registered',
  type: 'email',
  subject: 'Привет, Дружище!',
  content: `<!DOCTYPE html>
<html lang="ru">
<head><title>Добро пожаловать!</title></head>
<body>
<h1>Привет {{ name }}!</h1>
<p>Рады приветствовать тебя в нашем кинотеатре!</p>
</body>
</html>`
});
