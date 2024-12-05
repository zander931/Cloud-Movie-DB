# pylint: disable=unused-variable

'''API for movies'''
from datetime import datetime
from flask import Flask, jsonify, request
from database import (
    get_movies, get_movie_by_id, create_movie,
    update_movie, delete_movie, get_movies_by_genre, get_movie_by_country)

app = Flask(__name__)


def validate_sort_by(sort_by):
    '''Return if sort query is valid'''
    return sort_by in {'movie_id', 'title', 'score', 'budget', 'revenue'}


def validate_sort_order(order_by):
    '''Return if order query is valid'''
    return order_by in {'asc', 'desc'}


@app.route("/", methods=["GET"])
def endpoint_index():
    '''Landing'''
    return jsonify({"message": "Welcome to the Movie API",
                    "endpoints": {
                        "@app.route('/genres/<int:genre_id > '": "methods=['GET'])",
                        "@app.route('/countries/<string:country_code > '": "methods=['GET'])",
                        "@app.route('/movies/<int:movie_id > '": "methods=['GET', 'PATCH', 'DELETE'])",
                        "@app.route('/movies'": "methods=['GET', 'POST'])"}})


@app.route("/movies", methods=["GET", "POST"])
def endpoint_get_movies():
    '''Display or add movies'''
    response = {}
    status_code = 200
    if request.method == "GET":
        sort_by = request.args.get("sort_by", 'movie_id')
        sort_order = request.args.get("sort_order", 'asc')
        search = request.args.get("search")

        if not validate_sort_by(sort_by):
            response = {"error": "Invalid sort_by parameter"}
            status_code = 400

        if not validate_sort_order(sort_order):
            response = {"error": "Invalid sort_order parameter"}
            status_code = 400

        movies = get_movies(search, sort_by, sort_order)

        if not movies:
            response = {"error": "No movies found"}
            status_code = 404

        response = movies

    else:
        data = request.json
        columns = {
            "title": data.get("title"),
            "release_date": data.get("release_date"),
            "genre": data.get("genre"),
            "overview": data.get("overview"),
            "status": data.get("status"),
            "budget": data.get("budget", 0),
            "revenue": data.get("revenue", 0),
            "country": data.get("country"),
            "language": data.get("language"),
            "orig_title": data.get("orig_title"),
            "score": data.get("score")
        }

        if not all([columns['title'], columns['release_date'],
                   columns['genre'], columns['country'], columns['language']]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            datetime.strptime(columns['release_date'], "%m/%d/%Y")
        except ValueError:
            return jsonify({"error": "Invalid release_date format. Please use MM/DD/YYYY"}), 400

        try:
            movie = create_movie(columns)
            return jsonify({'success': True, "movie": movie}), 201
        except (KeyError, TypeError, ValueError, AttributeError, IndexError) as e:
            return jsonify({"error": str(e)}), 500

    return jsonify(response), status_code


@app.route("/movies/<int:movie_id>", methods=["GET", "PATCH", "DELETE"])
def endpoint_get_movie(movie_id: int):
    '''GET, PATCH OR DELETE a movie given its ID'''
    response = {}
    status_code = 200
    if request.method == "PATCH":
        data = request.json
        columns = {
            "title": data.get("title"),
            "release_date": data.get("release_date"),
            "genre": data.get("genre"),
            "overview": data.get("overview"),
            "status": data.get("status"),
            "budget": data.get("budget"),
            "revenue": data.get("revenue"),
            "country": data.get("country"),
            "language": data.get("language"),
            "orig_title": data.get("orig_title"),
            "score": data.get("score")
        }

        if not any([columns['title'], columns['release_date'], columns['genre'],
                    columns['overview'], columns['status'], columns['budget'],
                    columns['revenue'], columns['country'], columns['language']]):
            response = {"error": "No fields to update"}
            status_code = 400

        try:
            movie = update_movie(movie_id, columns)
            response = {'success': True, "movie": movie}
        except (KeyError, TypeError, ValueError, AttributeError, IndexError) as e:
            response = {"error": str(e)}
            status_code = 500

    elif request.method == "GET":

        movie = get_movie_by_id(movie_id)

        if not movie:
            response = {"error": "Movie not found"}
            status_code = 404

        return jsonify(movie), 200

    else:
        success = delete_movie(movie_id)

        if not success:
            return jsonify({"error": "Movie could not be deleted"}), 404

        return jsonify({"message": "Movie deleted"})

    return jsonify(response), status_code


@app.route("/countries/<string:country_code>", methods=["GET"])
def endpoint_get_movies_by_country(country_code: str):
    """Get a list of movie details by country. Optionally, the results 
    can be sorted by a specific field in ascending or descending order."""

    sort_by = request.args.get("sort_by", 'movie_id')
    sort_order = request.args.get("sort_order", 'asc')

    if not validate_sort_by(sort_by):
        return jsonify({"error": "Invalid sort_by parameter"}), 400

    if not validate_sort_order(sort_order):
        return jsonify({"error": "Invalid sort_order parameter"}), 400

    movies = get_movie_by_country(country_code, sort_by, sort_order)

    if not movies:
        return jsonify({"error": "No movies found for this country"}), 404

    return jsonify(movies)


@app.route("/genres/<int:genre_id>", methods=["GET"])
def endpoint_get_movies_by_genre(genre_id: int):
    """Get a list of movie details by genre. Optionally, the results 
    can be sorted by a specific field in ascending or descending order."""

    movies = get_movies_by_genre(genre_id)

    if not movies:
        return jsonify({"error": "No movies found for this country"}), 404

    return jsonify(movies)


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)
