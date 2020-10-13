# Comment Search

## Backend
Start the postgres database with
```shell script
docker run --name search-postgres -p 5432:5432 -e POSTGRES_PASSWORD=pw -e POSTGRES_DB=search -d postgres
```
