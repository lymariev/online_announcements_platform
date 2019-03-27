# Онлайн площадка для объявлений

#### REST API для веб-приложения “Онлайн площадка для объявлений”.

##### Развертывание приложения:

```bash
git clone https://github.com/Stinesc/online_announcements_platform.git
cd online_announcements_platform
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
cd online_announcements_platform
sudo -u postgres psql

CREATE DATABASE online_announcements_platform_db;
CREATE USER online_announcements_platform_db_admin WITH PASSWORD '123';
ALTER USER online_announcements_platform_db_admin CREATEDB; (для тестов)
CTRL + D

python3 manage.py migrate
python3 manage.py loaddata db.json
celery -A online_announcements_platform worker -l info -B (в отдельном терминале)
python3 manage.py runserver
```

##### Основные фитчи:

- Swagger для ендпоинтов\
(GET http://127.0.0.1:8000/)
- Регистрация/авторизация пользователей\
(POST http://127.0.0.1:8000/rest-auth/registration/)\
(POST http://127.0.0.1:8000/rest-auth/login/) 
- CRUD операции для объявления.\
 Основные поля:
  - Наименование (тема)
  - Вложенная рубрика/категория\
  (GET http://127.0.0.1:8000/categories/)\
  (GET http://127.0.0.1:8000/categories/{id}/)
    - Пример вложенной категории :
      - Бытовая техника
        - Холодильник
        - Пылесоc
      - Спорт
        - Велосипеды
        - Лодки
  - Текст (до 5000 знаков) 
  - До 8 фото
  - Цена (+ галочка “Договорная”)
- Доска объявлений:
  - могут просматривать все пользователи\
  (GET http://127.0.0.1:8000/announcements/)
  - создание объявлений (для авторизованных)\
  (POST http://127.0.0.1:8000/announcements/)
  - список объявлений
    - фильтрация списка объявлений (по категориям и цене)\
    (GET http://127.0.0.1:8000/announcements/?category=4&price=80.00)
    - пагинация списка объявлений
  - только автор объявления может редактировать и удалять объявления\
  (PUT http://127.0.0.1:8000/announcements/{id}/)\
  (DELETE http://127.0.0.1:8000/announcements/{id}/)
- Автоматическое скрытие объявления через 30 дней после последней активности (создания/обновления объявления)
- Админка: для управления пользователями, объявлениями и категориями\
  (GET http://127.0.0.1:8000/admin/)
- Покрытие кода юнит-тестами\
  Запуск тестов:
  ```bash
  python3 manage.py test
  ```
- Мои избранные объявления: 
  - авторизованный пользователь на Доске объявлений может отметить любое объявление “В избранное”
  (POST http://127.0.0.1:8000/announcements/{id}/add-to-favorites/)
  - просмотр весь список объявлений “Мои избранные объявления”
  (GET http://127.0.0.1:8000/announcements/favorites/)
  - удаление объявления из избранных
  (DELETE http://127.0.0.1:8000/announcements/{id}/delete-from-favorites/)
- Авторизация с помощью социальных сетей\
  (POST http://127.0.0.1:8000/rest-auth/facebook/)\
  (POST http://127.0.0.1:8000/rest-auth/twitter/)
- Чат на веб-сокетах между авторизованным пользователем и автором сообщения (если он доступен онлайн)\
  Для тестирования чата откройте в браузере несколько вкладок (GET http://127.0.0.1:8000/) и запустите в них веб-консоль.\
  Выполните во всех консолях JavaScript код:
  ```javascript
    var chatSocket = new WebSocket(
            'ws://' + window.location.host +
            '/announcements/1/online-chat/');
    chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var message = data['message'];
            var username = data['username'];
            console.log(username, ': ', message);
        };
   ```
   Для отправки сообщения выполните в любой из консолей:
   ```javascript
    chatSocket.send(JSON.stringify({
                'message': 'Hello world!'
            }));
   ```