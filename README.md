## Установка зависимостей
Убедитесь, что у вас установлены все необходимые библиотеки, указанные в файле `requirements.txt`. Выполните следующую команду, чтобы установить все зависимости:
```angular2html
pip install -r requirements.txt
```
## Настройка .env
В корневой папке бота находится файл `.env`, в нём нужно указать следующую информацию:
```dotenv
TOKEN=BOT_TOKEN # Токен вашего дискорд бота
DB_LINK=MONGO_DB_URL # Ссылка для потключения к базе банных
LOG_CHANNEL_ID=1140966249250164766 # ID канала для логов транзакций
ADMIN_ROLE_ID=1141708165147267162 # ID роли админи
CROUPIER_ROLE_ID=1141708242217607248 # ID роли крупье
CASHIER_ROLE_ID=1141708330709037126 # ID роли касира
```
Установите соответствующие значения для каждого пункта. 
Подробнее о создании бесплатной базы данных MongoDB можно посмотреть в [**этом видео**](https://www.youtube.com/watch?v=jXgJyuBeb_o&ab_channel=MongoDB) 
или создайте базу данных самостоятельно на [**этом сайте**](https://www.mongodb.com/).


## Запуск бота
Теперь, когда зависимости установлены и файл .env настроен, вы можете запустить бота. Пропишите следующую команду:
```
python main.py
```