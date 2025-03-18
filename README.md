# Emission Analyzer API

To run this application, you must have Docker installed.

## Environment Variables
Create a `.env` file in the root directory of the project and use these environment variables:

```
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
API_PORT=
```

## Docker Commands
Once you have created the `.env` file and the environment variables, 
run `docker-compose build`. This will run the commands in the `Dockerfile` to set up the application.

After that, run `docker-compose up`.

## Testing
Once everything is running, you can check that it works by going to this URL: http://localhost:8000/emission_analyzer_api/

You can also check that the data is in the database by running 
`docker exec -it emission-analyzer-db psql -U user -d emissionanalyzer`  and then `SELECT * FROM emission_analyzer_api_user;`.