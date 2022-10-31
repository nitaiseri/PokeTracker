from data_base.constants.queries import *
import requests
from .constants.consts import *
from fastapi import HTTPException

def create_insert_query(table_name, rows):
    query = f'INSERT INTO {table_name} VALUES'
    for row in rows:
        row_string = str(row)[1:-1]
        query += f'({row_string}),'
    return query[:-1] + ";"

def validate_trainer_name(connection, trainer_name):
    with connection.cursor() as cursor:
        return_value = cursor.execute(GET_TRAINER_ID_BY_NAME.format(trainer_name=trainer_name))
        if return_value:
            return cursor.fetchall()[0]["trainer_id"]
        return return_value

def validate_pokemon_name(connection, pokemon_name):
    with connection.cursor() as cursor:
        return_value = cursor.execute(GET_POKEMOM_ID_BY_NAME.format(pokemon_name=pokemon_name))
        if return_value:
            return cursor.fetchall()[0]["pokemon_id"]
        return return_value
    
def validate_type(connection, type):
    with connection.cursor() as cursor:
        return cursor.execute(GET_TYPE_ID_BY_NAME.format(type_name=type))

def validate_ownership(connection, trainer_id, pokemon_id):
    with connection.cursor() as cursor:
        return_value = cursor.execute(CHECK_OWNERSHIP.format(pokemon_id=pokemon_id, trainer_id=trainer_id))
        return return_value

def get_pokemon_info(pokemon_id):
    pokemon_info = requests.get(POKEMON_URL + str(pokemon_id))
    if pokemon_info.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    return pokemon_info.json()

def get_species_info(species_url):
    species_info = requests.get(species_url)
    if species_info.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    return species_info.json()
        
def get_evolution_chain_info(evolution_chain_url):
    evolution_chain_info = requests.get(evolution_chain_url)
    if evolution_chain_info.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    return evolution_chain_info.json()

def get_pokemon_next_generation_id(pokemon_id):
    pokemon_info = get_pokemon_info(pokemon_id)
    species_info = get_species_info(pokemon_info["species"]["url"])
    evolution_chain_info = get_evolution_chain_info(species_info["evolution_chain"]["url"])
    evolution_chain = get_evolution_chain(evolution_chain_info["chain"])
    return get_next_id(pokemon_id, evolution_chain)

def get_evolution_chain(evolution_chain_info):
    curront_object = evolution_chain_info
    evolution_chain_id = []
    while curront_object["evolves_to"]:
        evolution_chain_id.append(int(curront_object["species"]["url"][-2]))
        curront_object = curront_object["evolves_to"][0]
    evolution_chain_id.append(int(curront_object["species"]["url"][-2]))
    return evolution_chain_id

def get_next_id(current_id, evolution_chain):
    current_id_index = evolution_chain.index(current_id)
    if current_id_index < len(evolution_chain) - 1:
        current_id_index += 1
    return evolution_chain[current_id_index]

