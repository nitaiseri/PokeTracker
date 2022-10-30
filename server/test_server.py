from urllib import response
from fastapi.testclient import TestClient
from unittest import mock
from server import app

client = TestClient(app)

# @mock.patch()
# @mock.patch()


# option 1 without mock
# Get pokemons by name
def test_get_pokemon_by_name():
    pokemone_name = "ditto"
    response = client.get(f"/pokemons/{pokemone_name}")
    response_data = response.json()
    data = response_data[0]
    assert data["name"] == pokemone_name


# Get pokemons by type eevee
def test_get_pokemons_by_type():
    type = "normal"
    response = client.get(f"/pokemons/?type={type}")
    response_data = response.json()
    data = response_data
    assert {"name": "eevee"} in data


# Get pokemons by type yanma    
def test_get_pokemons_by_types():
    type1 = "bug"
    type2 = "flying"
    response1 = client.get(f"/pokemons/?type={type1}")
    response_data1 = response1.json()
    response2 = client.get(f"/pokemons/?type={type2}")
    response_data2 = response2.json()
    assert {"name": "yanma"} in response_data1 and response_data2

# Get pokemons by name
def test_get_pokemon_by_name():
    pokemone_name = "venusaur"
    response = client.get(f"/pokemons/{pokemone_name}")
    response_data = response.json()
    data = response_data[0]
    assert data["name"] == pokemone_name

def test_get_pokemons_by_types():
    type1 = "grass"
    type2 = "grass"
    response1 = client.get(f"/pokemons/?type={type1}")
    response_data1 = response1.json()
    response2 = client.get(f"/pokemons/?type={type2}")
    response_data2 = response2.json()
    assert {"name": "venusaur"} in response_data1 and response_data2