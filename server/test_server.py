from urllib import response
from fastapi.testclient import TestClient
from unittest import mock
from server import app
import functools
client = TestClient(app)

# @mock.patch()
# @mock.patch()


# option 1 without mock

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

#Updated pokemon types
def test_pokemons_by_types():
    type1 = "grass"
    type2 = "poison"
    response1 = client.get(f"/pokemons/?type={type1}")
    response_data1 = response1.json()
    response2 = client.get(f"/pokemons/?type={type2}")
    response_data2 = response2.json()
    assert {"name": "venusaur"} in response_data1 and response_data2


#Get pokemons by owner
def test_get_pokemons_by_owner(): 
    trainer_name= "Drasna"
    pokemons = [{"name":"wartortle"}, {"name":"caterpie"},{"name":"beedrill"},{"name":"arbok"},
 {"name":"clefairy"}, {"name":"wigglytuff"},{"name":"persian"}, 
 {"name":"growlithe"}, {"name":"machamp"}, {"name":"golem"}, {"name":"dodrio"}, 
 {"name":"hypno"}, {"name":"cubone"}, {"name":"eevee"},{"name":"kabutops"}]
    response = client.get(f"/pokemons/?trainer_name={trainer_name}")
    data = response.json()
    assert functools.reduce(lambda i, j : i and j, map(lambda m, k: m == k, data, pokemons), True)
    


#Get owners of a pokemon
def test_get_owner_by_pokemon():
    pokemone_name = "charmander"
    trainers = [{"name":"Giovanni"},{"name":"Jasmine"},{"name":"Whitney"}]
    response = client.get(f"/trainers/?pokemon_name={pokemone_name}")
    response_data = response.json() 
    assert functools.reduce(lambda i, j : i and j, map(lambda m, k: m == k, trainers, response_data), True)


#Delete Pokemon of a Trainer
def delete_pokemon_of_trainer():
    pokemons=[{"name":"venusaur"},{"name":"charmander"},{"name":"squirtle"},{"name":"pidgeot"},{"name":"raticate"},{"name":"spearow"},{"name":"pikachu"},{"name":"raichu"},{"name":"nidoran-f"},{"name":"nidorina"},{"name":"nidoking"},{"name":"oddish"},{"name":"vileplume"},{"name":"diglett"},{"name":"poliwag"},{"name":"machamp"},{"name":"hitmonlee"},{"name":"magikarp"},{"name":"kabutops"}]
  
    pass