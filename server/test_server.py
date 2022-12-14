from urllib import response
from fastapi.testclient import TestClient
from unittest import mock as mock_patch
from fastapi import HTTPException
from server import app
import functools

client = TestClient(app)

# Get pokemons by type eevee

def test_get_pokemons_by_type():
    type = "normal"
    response = client.get(f"/pokemons?type={type}")
    response_data = response.json()
    data = response_data
    assert {"name": "eevee"} in data


# Get pokemons by type yanma
def test_get_pokemons_by_types():
    type1 = "bug"
    type2 = "flying"
    response1 = client.get(f"/pokemons?type={type1}")
    response_data1 = response1.json()
    response2 = client.get(f"/pokemons?type={type2}")
    response_data2 = response2.json()
    assert {"name": "yanma"} in response_data1 and response_data2

# Get pokemons by name
def test_get_pokemon_by_name():
    pokemone_name = "venusaur"
    response = client.get(f"/pokemons/{pokemone_name}")
    response_data = response.json()
    data = response_data[0]
    assert data["name"] == pokemone_name

# Updated pokemon types


def test_pokemons_by_types():
    type1 = "grass"
    type2 = "poison"
    response1 = client.get(f"/pokemons?type={type1}")
    response_data1 = response1.json()
    response2 = client.get(f"/pokemons?type={type2}")
    response_data2 = response2.json()
    assert {"name": "venusaur"} in response_data1 and response_data2


# Get pokemons by owner
def test_get_pokemons_by_owner():
    trainer_name = "Drasna"
    pokemons = [{"name": "wartortle"}, {"name": "caterpie"}, {"name": "beedrill"}, {"name": "arbok"},
                {"name": "clefairy"}, {"name": "wigglytuff"}, {"name": "persian"},
                {"name": "growlithe"}, {"name": "machamp"}, {
                    "name": "golem"}, {"name": "dodrio"},
                {"name": "hypno"}, {"name": "cubone"}, {"name": "eevee"}, {"name": "kabutops"}]
    response = client.get(f"/pokemons?trainer_name={trainer_name}")
    data = response.json()
    assert functools.reduce(lambda i, j: i and j, map(
        lambda m, k: m == k, data, pokemons), True)


# Get owners of a pokemon
def test_get_owner_by_pokemon():
    pokemone_name = "charmander"
    trainers = [{"name": "Giovanni"}, {"name": "Jasmine"}, {"name": "Whitney"}]
    response = client.get(f"/trainers?pokemon_name={pokemone_name}")
    response_data = response.json()
    assert functools.reduce(lambda i, j: i and j, map(
        lambda m, k: m == k, trainers, response_data), True)


# evolve Pokemon
def test_evolve_max_evolvment():
    trainer_name = "Whitney"
    pokemone_name = "venusaur"
    response = client.patch(
        f"/pokemons/evolve?pokemon_name={pokemone_name}&trainer_name={trainer_name}")
    response_data = response.json()
    assert response_data["detail"] == F"{pokemone_name} cannot evolve. He is already the best version of itself."


def test_evolve_not_exist():
    trainer_name = "Archie"
    pokemone_name = "spearow"
    response = client.patch(
        f"/pokemons/evolve?pokemon_name={pokemone_name}&trainer_name={trainer_name}")
    response_data = response.json()
    assert response_data["detail"] == F"{trainer_name} does not own {pokemone_name}."

# Delete Pokemon of a Trainer
@mock_patch('data_base.db_manager.delete_pokemon_of_specific_trainer')
def test_delete_pokemon_of_trainer(delete_pokemon_of_specific_trainer):
    delete_pokemon_of_specific_trainer.side_effect = HTTPException
    pokemon_name = "venusaur"
    trainer_name = "Nit"
    deleted_pokemon = {"name": "venusaur"}
    pokemons = [{"name": "venusaur"}, {"name": "charmander"}, {"name": "squirtle"}, {"name": "pidgeot"}, {"name": "raticate"}, {"name": "spearow"}, {"name": "pikachu"}, {"name": "raichu"}, {"name": "nidoran-f"},
                {"name": "nidorina"}, {"name": "nidoking"}, {"name": "oddish"}, {"name": "vileplume"}, {"name": "diglett"}, {"name": "poliwag"}, {"name": "machamp"}, {"name": "hitmonlee"}, {"name": "magikarp"}, {"name": "kabutops"}]
    client.delete(f"/pokemons/{pokemon_name}/trainers/{trainer_name}")
    response = client.get(f"/pokemons?trainer_name={trainer_name}")
    response_data = response.json()
    assert all(pokemon_object in pokemons for pokemon_object in response_data) and (
        deleted_pokemon not in response_data)
