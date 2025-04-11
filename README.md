# Emission Analyzer API

## Prerequisites
Ensure you have Docker installed and the emission-analyzer-model repository cloned before running this application.

## Environment Variables
Create a `.env` file in the root directory of the project and define the following variables:

```
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
API_PORT=
APP_PORT=
PATH_TO_MODEL=
MODEL_PORT=
```

`PATH_TO_MODEL` is the relative path to the `emission-analyzer-model` directory on your local machine.

`APP_PORT` defaults to 5173 if not set in the `.env` file.

## Running the Application
1. Build the Docker container by running:
    ```
    docker-compose build
    ```

2. Start the containers by running:
    ```
    docker-compose up
    ```

## Development
* Verify the server is running by visiting: `http://localhost:{API_PORT}/emission_analyzer_api/`

* To create migrations, run:
    ```
    docker exec -it emission-analyzer-api python manage.py makemigrations
    ```
* To execute migrations, run:
    ```
    docker exec -it emission-analyzer-api python manage.py migrate
    ```
* Connect to the database by running:
    ```
    docker exec -it emission-analyzer-db psql -U user -d {POSTGRES_NAME}
    ```
    Next, run:
    ```
    \dt
    ```
    You should see all the data tables. The data tables created from our migrations should start with `emission_analyzer_api`.
    
## References
* [psql Meta-Commands](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-PATTERNS)

* [SQL Commands Supported by PostgreSQL](https://www.postgresql.org/docs/current/sql-commands.html)

* [Django Documentation](https://docs.djangoproject.com/en/5.2/)