from urllib import response
from fastapi.testclient import TestClient
from unittest import mock
import sys
sys.path.append("..")
from server.server import app

client = TestClient(app)

@mock.patch()
def test_get_pokemon_by_name():
    pokemone_name = "ditto"
    response = client.get(f"/pokemons/{pokemone_name}")
    response_data = response.json()
    assert response_data.name == pokemone_name


@mock.patch()
def get_pokemons_by_parameters():
    pass