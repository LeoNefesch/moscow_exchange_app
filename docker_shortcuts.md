Сборка / персборка контейнера:
```commandline
sudo docker-compose up -d
```
Остановка и удаление контейнера (если в docker-compose внесены изменения):
```commandline
sudo docker-compose down
```
Информация о контейнерах:
```commandline
sudo docker-compose ps
```
Логи:
```commandline
sudo docker-compose logs postgres <или другое имя сервиса>
```

Список томов:
```commandline
sudo docker volume ls
```
Удалить том (потребуется перед удалением БД):
```commandline
sudo docker volume rm <имя тома>
```