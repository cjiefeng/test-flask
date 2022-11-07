# Flask app template

## Local test

1. Spin up docker images, docker compose includes app & MySQL 8.0.
   ```
   $ docker-compose up
   ```
2. Initial start up: in another terminal, exec into app image and run db migration command
   ```
   $ docker exec -ti flask_app flask initdb
   ```
3. DB changes required: in another terminal, exec into db image and run changes
   ```
   $ docker exec -ti flask_db bash
   $ mysql -uroot -pMYSQL_ROOT_PASSWORD
   mysql > -- run sql changes;
   ```
4. Access api from localhost:5050
   ```
   $ curl 127.0.0.1:5050/api/example/get_all_items
   ```
