Docs for Docker - Postgres Setup
#### Version

Cmd 1: docker run -d --name postgresdb -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -v /data:/var/lib/postgresql/data postgres

Cmd 2: docker run -d --name pgadminui -p 8080:80 -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=admin -d dpage/pgadmin4

OR docker-compose up -d

cmd 3: docker inspect <container id for pgadmin>

pgadmin Settings
1. Host Name/Address -> container gateway address or container name(postgresbd)
2. Port ->  container host port(5455)
3. Username -> POSTGRES_USER ()
4. Password -> POSTGRES_PASSWORD



# Be keen to change volumes local path to avoid authentication issues/conflicts due to a previous db using the same persistent path

https://medium.com/quick-code/how-to-run-postgresql-and-pgadmin-using-docker-90638fde8bf
https://belowthemalt.com/2021/06/09/run-postgresql-and-pgadmin-in-docker-for-local-development-using-docker-compose/
https://hevodata.com/learn/docker-postgresql/