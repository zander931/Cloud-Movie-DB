"""A script to import all of the movies in imdb_movies.csv into the database"""
from os import environ  # Gives the program access to the environment variables

from dotenv import load_dotenv  # Loads variables from a file into the environment
import csv
import psycopg2
import psycopg2.extras


def get_connection():
    conn = psycopg2.connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )
    return conn


def get_cursor(conn):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor


def load_csv(filename: str) -> list[dict]:
    movies = []
    with open(filename, encoding="utf-8") as f:
        for line in csv.DictReader(f):
            movies.append(line)
    return movies


def get_language_id(language: str) -> int:
    language = language.strip()
    cursor.execute(  # pylint: disable=E0606
        "SELECT language_id FROM language WHERE language_name = %s", (language,))
    conn.commit()  # pylint: disable=E0606
    return cursor.fetchone()[0]


def get_country_id(country: str) -> int:
    cursor.execute(
        "SELECT country_id FROM country WHERE country_name = %s", (country,))
    conn.commit()
    return cursor.fetchone()[0]


def get_genre_id(genre: str) -> int:
    genre = genre.strip()
    cursor.execute(
        "SELECT genre_id FROM genre WHERE genre_name = %s", (genre,))
    conn.commit()
    return cursor.fetchone()[0]


def import_movies_to_database(movies: list[dict]) -> None:
    query = '''INSERT INTO movie (title, release_date, score,
                overview, orig_title, status, orig_lang, budget,
                revenue, country) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING movie_id;'''

    genre_query = '''INSERT INTO movie_genres (movie_id, genre_id)
                     VALUES (%s, %s);'''

    for movie in movies:
        language_id = get_language_id(movie['orig_lang'])
        country_id = get_country_id(movie['country'])
        cursor.execute(
            query, (movie['names'], movie['date_x'], movie['score'], movie['overview'],
                    movie['orig_title'], movie['status'].strip(), language_id,
                    movie['budget_x'], movie['revenue'], country_id))
        movie_id = cursor.fetchone()[0]
        print(movie_id)
        conn.commit()

        genre_list = movie['genre'].split(",")
        if genre_list == ['']:
            genre_list = ['No Genre']
        for genre in genre_list:
            genre_id = get_genre_id(genre)
            cursor.execute(
                genre_query, (movie_id, genre_id)
            )
            conn.commit()


if __name__ == "__main__":
    load_dotenv('.env.prod')
    conn = get_connection()
    cursor = get_cursor(conn)
    movies = load_csv("imdb_movies.csv")
    import_movies_to_database(movies)
    cursor.execute("SELECT * FROM movie")
    conn.commit()
    rows = cursor.fetchall()
    print(rows)
