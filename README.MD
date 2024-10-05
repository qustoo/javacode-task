# Состав проекта

Тестовое задание - 
 ```
 https://docs.google.com/document/d/1hEnCQnhljJ-pAwg7coi31J_3A05ctPcysIdkIuHXRqs/edit?pli=1\
 ```

Кодовая база находится в папке '/app'

- Тестовое задание выполнено на языке Python при помощи фреймворка FastAPI.
- База данных - PostgreSQL
- ORM - SQlAlchemy
- Линтеры - flake8, isort,black
- Порт для доступа к апишке - 8080
- Сборка и развертывание через docker, docker-compose


Сборка выполняется при docker-compose.yml и Makefile'а

+ ***Поднять приложение***```make up```
+ ***Остановить приложение***```make up```
+ ***Собрать образ***```make build```
+ ***Посмотреть логи***```make logs```
+ ***Прогнать все линтеры***```make linters```



