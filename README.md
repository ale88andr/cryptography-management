# Корень проекта
В нём находятся базовые вещи, например,
Dockerfile, ci и gitignore

# src
Cодержит исходный код приложения.

# main.py
Входная точка приложения.

# api
Ммодуль, в котором реализуется API. Другими словами, это модуль для предоставления http-интерфейса клиентским
приложениям. Внутри модуля отсутствует какая-либо бизнес-логика, так как она не должна быть завязана на HTTP.

# core
Содержит разные конфигурационные файлы.

# db
Предоставляет объекты баз данных (Redis, Elasticsearch) и провайдеры для внедрения зависимостей. Redis будет
использоваться для кеширования, чтобы не нагружать лишний раз Elasticsearch.

# models
Содержит классы, описывающие бизнес-сущности, например, фильмы, жанры, актёров.

# services
В этом модуле находится реализация всей бизнес-логики. Таким образом она отделена от транспорта.
Благодаря такому разделению, вам будет легче добавлять новые типы транспортов в сервис.
Например, легко добавить RPC протокол поверх AMQP или Websockets.

# Запуск проекта

Выгрузить дамп базы данных (если требуется)

```Shell
pg_dump -Fc -b cm2 > cm2.dump
```
Запустить контейнер

```Shell
docker compose up --build
```

Загрузить дамп базы данных (если требуется)

```Shell
docker exec db pg_restore --verbose --clean --if-exists --exit-on-error --dbname cm2 cm2.dump --single-transaction
```
