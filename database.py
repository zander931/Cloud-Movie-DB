# pylint: disable=unused-variable
'''Handle requests using database'''

from os import environ  # Gives the program access to the environment variables
from datetime import datetime
from typing import Any
import psycopg2
import psycopg2.extras

from dotenv import load_dotenv  # Loads variables from a file into the environment


def get_connection():
    '''Get connection'''

    load_dotenv('.env.prod')

    return psycopg2.connect(
        user=environ["DATABASE_USERNAME"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )


def get_cursor(conn):
    '''Return cursor'''
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_entire_movie(response):
    '''Return list of all movies in response'''
    return [
        {'Movie ID': i['movie_id'], 'Title': i['title'], 'Release Date': i['release_date'],
         'Score': i['score'], 'Overview': i['overview'], 'Original Title': i['orig_title'],
         'Status': i['status'], 'Original Language': i['orig_lang'], 'Budget': i['budget'],
         'Revenue': i['revenue'], 'Country': i['country']} for i in response
    ]


def get_movies(search: str = None, sort_by: str = None, sort_order: str = None) -> list[dict]:
    '''Retrieve all movies'''
    conn = get_connection()
    cursors = get_cursor(conn)

    query = "SELECT * FROM movie"
    params = []

    if search:
        query += " WHERE title ILIKE %s"
        params.append(f"%{search}%")
    if sort_by and sort_order:
        query += f" ORDER BY {sort_by} {sort_order.upper()}"

    cursors.execute(query, params)
    conn.commit()
    response = cursors.fetchall()
    print(len(response))

    return get_entire_movie(response)


def get_movie_by_id(movie_id: int) -> dict[str, Any]:
    '''Retrieve movie given a movie ID'''
    conn = get_connection()
    cursors = get_cursor(conn)

    cursors.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    conn.commit()

    response = cursors.fetchall()
    return get_entire_movie(response)


def create_movie(columns) -> dict:
    '''POST request'''

    conn = get_connection()
    cursors = get_cursor(conn)

    cursors.execute(
        "SELECT language_id FROM language WHERE language_name = %s", (columns['language'],))
    conn.commit()

    language_id = cursors.fetchone()['language_id']

    cursors.execute(
        "SELECT country_id FROM country WHERE country_name = %s", (columns['country'],))
    conn.commit()

    country_id = cursors.fetchone()['country_id']

    convert_release_date = datetime.strptime(
        columns['release_date'], "%m/%d/%Y")

    query = '''INSERT INTO movie (title, release_date, score,
                overview, orig_title, status, orig_lang, budget,
                revenue, country) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING movie_id;'''
    params = (columns['title'], convert_release_date, columns['score'],
              columns['overview'], columns['orig_title'], columns['status'],
              language_id, columns['budget'], columns['revenue'], country_id)

    cursors.execute(query, params)
    conn.commit()

    movie_id = cursors.fetchone()['movie_id']

    genre_list = columns['genre'].split(",")

    for genres in genre_list:
        genres = genres.strip()
        cursors.execute(
            "SELECT genre_id FROM genre WHERE genre_name = %s", (genres,))
        conn.commit()

        genre_id = cursors.fetchone()['genre_id']

        cursors.execute('''INSERT INTO movie_genres (movie_id, genre_id)
                        VALUES (%s, %s)''', (movie_id, genre_id))
        conn.commit()

    cursors.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    conn.commit()

    response = cursors.fetchall()

    return get_entire_movie(response)


def update_movie(movie_id: int, columns) -> dict[str, Any]:
    '''PATCH request'''
    conn = get_connection()
    cursors = get_cursor(conn)

    cursors.execute(
        "SELECT language_id FROM language WHERE language_name = %s", (columns['language'],))
    conn.commit()
    language_id = cursors.fetchone()['language_id']

    cursors.execute(
        "SELECT country_id FROM country WHERE country_name = %s", (columns['country'],))
    conn.commit()
    country_id = cursors.fetchone()['country_id']

    query = '''UPDATE movie SET
               title = %s, release_date = %s, score = %s, overview = %s,
               orig_title = %s, status = %s, orig_lang = %s, budget = %s,
               revenue = %s, country = %s
               WHERE movie_id = %s'''

    params = (columns['title'], columns['release_date'], columns['score'],
              columns['overview'], columns['orig_title'], columns['status'],
              language_id, columns['budget'], columns['revenue'],
              country_id, columns['movie_id'])

    cursors.execute(query, params)
    conn.commit()

    cursors.execute(
        "DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
    conn.commit()

    genre_list = columns['genre'].split(",")

    for genres in genre_list:
        genres = genres.strip()
        cursors.execute(
            "SELECT genre_id FROM genre WHERE genre_name = %s", (genres,))
        conn.commit()

        genre_id = cursors.fetchone()['genre_id']

        cursors.execute('''INSERT INTO movie_genres (movie_id, genre_id)
                        VALUES (%s, %s)''', (movie_id, genre_id))
        conn.commit()

    cursors.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    conn.commit()
    response = cursors.fetchall()

    return get_entire_movie(response)


def delete_movie(movie_id: int) -> bool:
    '''DELETE request'''
    conn = get_connection()
    cursors = get_cursor(conn)

    cursors.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    conn.commit()

    movie = cursors.fetchone()
    if not movie:
        return False

    cursors.execute(
        "DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))

    cursors.execute("DELETE FROM movie WHERE movie_id = %s", (movie_id,))
    conn.commit()
    return True


def get_movies_by_genre(genre_id: int) -> list[dict[str, Any]]:
    '''Return movies that have the given genre'''
    conn = get_connection()
    cursors = get_cursor(conn)

    query = '''SELECT movie.* FROM movie JOIN movie_genres
               ON movie.movie_id = movie_genres.movie_id
               WHERE movie_genres.genre_id = %s'''

    cursors.execute(query, (genre_id,))
    conn.commit()
    response = cursors.fetchall()

    return get_entire_movie(response)


def get_movie_by_country(country_code, sort_by: str = None, sort_order: str = None) -> list[dict]:
    '''Retrieve the country given the country code'''
    conn = get_connection()
    cursors = get_cursor(conn)

    query = f'''SELECT * FROM movie JOIN country
               ON movie.country = country.country_id
               WHERE country.country_name = '{country_code}\''''

    if sort_by and sort_order:
        query += f" ORDER BY {sort_by} {sort_order.upper()}"

    cursors.execute(query)
    conn.commit()
    response = cursors.fetchall()

    return get_entire_movie(response)
