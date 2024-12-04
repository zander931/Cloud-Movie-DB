# The Movie API + DB

## Description

This is a simple API that allows you to manage a movie database. You can add, delete, update and list movies. The API is built using Flask and the database is Postgres.

## Files

- `api.py`: The main file that contains the API.
- `test_api.py`: A test file that tests the API.
- `import.py`: A script that imports a list of movies from a CSV file into the database.
- `imdb_movies.csv`: A CSV file containing a list of movies.
- `schema.sql`: The SQL file that contains the database schema.

## Environment Variables

All of the following environment variables must be set in order to run the API. They must be in a file named `.env` in the root directory of the project.

- `DATABASE_USERNAME`: The username of the database.
- `DATABASE_PASSWORD`: The password of the database.
- `DATABASE_IP`: The IP address of the database.
- `DATABASE_PORT`: The port of the database.
- `DATABASE_NAME`: The name of the database.