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
* Verify the API is running by visiting: http://localhost:8000/emission_analyzer_api/

* Check the database by running:
    ```
    docker exec -it emission-analyzer-db psql -U user -d emissionanalyzer
    ```
    Then execute:
    ```
    SELECT * FROM emission_analyzer_api_user;
    ```