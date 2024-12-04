# pylint: disable=unused-variable
'''Test api file'''
import pytest
from api import app


@pytest.fixture(name='client')
def test_client():
    '''Test client'''
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_endpoint_index(client):
    '''Test endpoint index'''
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}


def test_endpoint_get_movies(client):
    '''Test endpoint get movies'''
    response = client.get("/movies")
    assert response.status_code == 200


def test_endpoint_get_movie(client):
    '''Test endpoint get movie'''
    response = client.get("/movies/1")
    assert response.status_code == 200
