# Emission Analyzer API

## Prerequisites
Ensure you have Docker installed before running this application.

## Environment Variables
Create a `.env` file in the root directory of the project and define the following variables:

```
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
API_PORT=
```

## Running the Application
1. Build the Docker container by running:
    ```
    docker-compose build
    ```
    This command executes the instructions in the `Dockerfile` to set up the application.

2. Start the containers by running:
    ```
    docker-compose up
    ```

## Testing
* Verify the server is running by visiting: `http://localhost:{API_PORT}/emission_analyzer_api/`

* For migrations, run:
    ```
    docker exec -it emission-analyzer-api python manage.py migrate
    ```
* Check the database by running:
    ```
    docker exec -it emission-analyzer-db psql -U user -d {POSTGRES_NAME}
    ```
    Then execute:
    ```
    \dt
    ```
    You should see all the data tables. 
    
## References
* [psql Meta-Commands](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-PATTERNS)

* [SQL Commands Supported by PostgreSQL](https://www.postgresql.org/docs/current/sql-commands.html)