from constants.consts import *
from constants.queries import *
from dtos import *
from unicodedata import name
import pymysql
import sys
import json
import requests

from fastapi import HTTPException

def create_db(name):
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            query = 'CREATE DATABASE ' + name
            cursor.execute(query)
            connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def execute_queries(data_base_name, queries):
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db=data_base_name,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def create_insert_query(table_name, rows, has_id):
    query = f'INSERT INTO {table_name} VALUES'
    id = "" if has_id else "null, "
    for row in rows:
        row_string = str(row)[1:-1]
        query += f'({id}{row_string}),'
    return query[:-1] + ";"
    
def run():
    create_db(DB_NAME)
    execute_queries(DB_NAME, tables_creation_queries)
    init_tables_from_api()

def init_tables_from_api():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db=DB_NAME,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            init_type_table(cursor)
            init_pokemon_table(cursor)  # Init pokemon and pokemon-type tables
            # init_tables_from_json(cursor, JSON_PATH)
            # init_trainer_table()  # Init trainer and pokemon-trainer tables
        connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def init_type_table(cursor):
    result = requests.get(TYPES_URL)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    data = result.json()
    type_list = data["results"]
    type_values = []
    for type in type_list:
        id = int(type["url"].split("/")[-2])
        type_values.append([id, type["name"]])
    query = create_insert_query(table_name=TYPE_TABLE, rows=type_values, has_id=True)
    cursor.execute(query)

def init_pokemon_table(cursor):
    result = requests.get(POKEMONS_URL)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    dto_pokemon = DtoPokemon(pokemons_object=result.json())
    values_pokemon_table = []
    values_pokemon_types_table = []
    for pokemon_object in dto_pokemon.results:
        pokemon = get_pokemon(pokemon_object["url"])
        values_pokemon_table.append([pokemon.id,pokemon.name,pokemon.height,pokemon.weight])
        for type in pokemon.types_ids:
            values_pokemon_types_table.append([pokemon.id,type])

    query_pokemon_table = create_insert_query(table_name=POKEMON_TABLE, rows=values_pokemon_table, has_id=True)
    query_pokemon_type_table = create_insert_query(table_name=POKEMON_TYPE_TABLE, rows=values_pokemon_types_table, has_id=True)
    cursor.execute(query_pokemon_table)
    cursor.execute(query_pokemon_type_table)

        

def get_pokemon(url):
    result = requests.get(url)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    return Pokemon(pokemon_object=result.json())
    



























def init_tables_from_json(cursor, json_path):
    with open(json_path) as f:
        data = json.load(f)
    for pokemon in data:
        insert_pokemon_data_to_tables(pokemon, cursor)

def init_trainer_table():
    pass



def get_pokemon_type_list(pokemon_id):
    result = requests.get(POKEMONS_URL + pokemon_id)
    data = result.json()
    return [t["type"]["name"] for t in data["types"]]

def insert_pokemon_data_to_tables(pokemon_object, cursor):
    pokemon = Pokemon(pokemon_object)
    pokemon_query = create_insert_query(POKEMON_TABLE, [pokemon.get_items()], True)
    cursor.execute(pokemon_query)
    types = get_pokemon_type_list(pokemon.get_id())
    types_id = [cursor.excute(f'SELECT type_id FROM {TYPE_TABLE} WHERE name={name}') for name in types]
    # types_query = create_insert_query(TYPE_TABLE, , False)
    # cursor.execute(types_query)
    for trainer in pokemon_object["ownedBy"]:
        trainer_values = [trainer["name"], trainer["town"]]
        query = create_insert_query(TRAINER_TABLE, trainer_values, False)
        try:
            cursor.execute(query)
        except:
            pass
        cursor.execute(
            f"SELECT trainer_id FROM trainer WHERE name='{trainer['name']}' AND town='{trainer['town']}'")
        trainer_id = cursor.fetchall()[0]["trainer_id"]
        query = create_insert_query(POKEMON_TRAINER_TABLE, [
                                    pokemon_object["id"], trainer_id], True)
        cursor.execute(query)





if __name__ == "__main__":
    run()
    
    # insert_all_json_data(DB_NAME, "pokemons.json")
