# Online announcements platform

## How to run

#### Clone project:
```bash
git clone https://github.com/Stinesc/ingredient_order_site.git
```
#### Install PostgreSQL:
```bash
sudo apt-get install postgresql
```
#### Start PostgreSQL console:
```bash
sudo -u postgres psql
```
#### Create database and user:
```bash
CREATE DATABASE online_announcements_platform_db;
CREATE USER online_announcements_platform_db_admin WITH PASSWORD '123';
ALTER USER online_announcements_platform_db_admin CREATEDB; (for tests)
CTRL + D
```
#### Create, activate virtual environment and install packages:
```bash
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
```
#### Make migrations and migrate:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
#### Create superuser:
```bash
python3 manage.py createsuperuser
```
#### Run Celery (in a separate terminal):
```bash
sudo apt-get install redis
celery -A online_announcements_platform worker -l info -B
```
#### Run server:
```bash
python3 manage.py runserver
```
#### Run tests:
```bash
python3 manage.py test
```
#### Test WebSockets:
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
chatSocket.send(JSON.stringify({
            'message': 'Hello world!'
        }));
```