from constants.consts import *
from constants.queries import *
from dtos import *
import pymysql
import sys
import json
import requests
from fastapi import HTTPException
db_connection = connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db=DB_NAME,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

def create_db(data_base_name):
    try:
        global db_connection
        with db_connection.cursor() as cursor:
            query = 'CREATE DATABASE ' + data_base_name
            cursor.execute(query)
            db_connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def execute_queries(queries):
    try:
        global connection
        with connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def create_insert_query(table_name, rows):
    query = f'INSERT INTO {table_name} VALUES'
    for row in rows:
        row_string = str(row)[1:-1]
        query += f'({row_string}),'
    return query[:-1] + ";"
    
def init_tables():
    try:
        global connection
        with connection.cursor() as cursor:
            init_type_table(cursor)
            init_pokemon_table(cursor)  # Init pokemon and pokemon-type tables
            init_tables_from_json(cursor, JSON_PATH) # Init Trainer and pokemon-trainer tables
        connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def get_pokemon(url):
    result = requests.get(url)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    return Pokemon(pokemon_object=result.json())

def init_types(result):
    type_list = result.json()["results"]
    type_values = []
    for type in type_list:
        id = int(type["url"].split("/")[-2])
        type_values.append([id, type["name"]])
    return type_values

def init_type_table(cursor):
    result = requests.get(TYPES_URL)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    type_values = init_types(result)    
    query = create_insert_query(table_name=TYPE_TABLE, rows=type_values)
    cursor.execute(query)

def get_pokemon_insert_values_from_json(dto_pokemon):
    values_pokemon_table = []
    values_pokemon_types_table = []
    print(f"Start read pokemons")
    for i, pokemon_object in enumerate(dto_pokemon.results):
        pokemon = get_pokemon(pokemon_object["url"])
        values_pokemon_table.append([pokemon.id,pokemon.name,pokemon.height,pokemon.weight])
        for type in pokemon.types_ids:
            values_pokemon_types_table.append([pokemon.id,type])
        print(f"read {i}, out of {len(dto_pokemon.results)}")
    return values_pokemon_table,values_pokemon_types_table

def get_trainer_insert_values_from_json(json_data):
    trainer_exist, trainer_dict, trainer_id_counter = False, dict(), 1
    values_trainer_table, values_pokemon_trainer_table = [], []
    for pokemon in json_data:
        pokemon_id = pokemon.get("id")
        for raw_trainer in pokemon.get("ownedBy"):
            trainer = Trainer(raw_trainer)
            trainer_exist = (trainer.name, trainer.town) in trainer_dict.keys()
            if not trainer_exist:
                trainer_dict[(trainer.name, trainer.town)] = trainer_id_counter
                values_trainer_table.append([trainer_id_counter, trainer.name, trainer.town])
                trainer_id_counter += 1
            trainer_id = trainer_dict[(trainer.name, trainer.town)]
            values_pokemon_trainer_table.append([pokemon_id, trainer_id])
    return values_trainer_table, values_pokemon_trainer_table   

def execute_insert_query(cursor, table_name, values_list):
    query = create_insert_query(table_name = table_name,rows = values_list)
    cursor.execute(query)

def init_pokemon_table(cursor):
    result = requests.get(POKEMONS_URL)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    dto_pokemon = DtoPokemon(pokemons_object=result.json())
    values_pokemon_table, values_pokemon_types_table = get_pokemon_insert_values_from_json(dto_pokemon) 
    execute_insert_query(cursor = cursor, table_name = POKEMON_TABLE, values_list = values_pokemon_table)
    execute_insert_query(cursor = cursor, table_name = POKEMON_TYPE_TABLE, values_list = values_pokemon_types_table)
    
def init_tables_from_json(cursor, json_path):
    with open(json_path) as f:
        data = json.load(f)
    values_trainer_table, values_pokemon_trainer_table = get_trainer_insert_values_from_json(json_data=data)
    execute_insert_query(cursor = cursor, table_name = TRAINER_TABLE, values_list = values_trainer_table)
    execute_insert_query(cursor = cursor, table_name = POKEMON_TRAINER_TABLE, values_list = values_pokemon_trainer_table)

def run():
    create_db(data_base_name = DB_NAME)
    execute_queries(queries = tables_creation_queries)
    init_tables()


if __name__ == "__main__":
    run()
    