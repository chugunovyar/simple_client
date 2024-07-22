# Description:

Python 3.11
Git flow\Rebase

Пример простого клиента который взаимодействует с сервером отправляя ему запросы. 


# HOW TO USE

1. Запуск
```shell
docker compose up --build
```
2. Пример запроса для генерации запросов.
```shell
curl --location --request GET 'http://localhost:8001/run/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=gibvf60D84oizldNvyNg6P3OMUT3l6XO' \
--data '{"num": 100}'
```

3. 