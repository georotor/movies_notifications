db.templates.insertOne({
  name: 'Регистрация нового пользователя',
  event: 'registered',
  type: 'email',
  content: `<!DOCTYPE html>
<html lang="ru">
<head><title>Добро пожаловать!</title></head>
<body>
<h1>Привет {{ name }}!</h1>
<p>Рады приветствовать тебя в нашем кинотеатре!</p>
</body>
</html>`
});
