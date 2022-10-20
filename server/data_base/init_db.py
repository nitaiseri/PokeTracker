from typing import List
from constants.consts import *
from constants.queries import *
from dtos import *
from unicodedata import name
import pymysql
import sys
import os
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

def create_insert_query(table_name, rows):
    query = f'INSERT INTO {table_name} VALUES'
    for row in rows:
        row_string = str(row)[1:-1]
        query += f'({row_string}),'
    return query[:-1] + ";"
    
def run():
    # create_db(DB_NAME)
    # execute_queries(DB_NAME, tables_query_pokemon_trainer)
    # execute_queries(DB_NAME, tables_creation_queries)
    # init_tables()
    pass

def init_tables():
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
            init_tables_from_json(cursor, JSON_PATH)
        connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)

def get_pokemon(url):
    result = requests.get(url)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    return Pokemon(pokemon_object=result.json())

def init_type_table(cursor):
    result = requests.get(TYPES_URL)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    type_list = result.json()["results"]
    type_values = []
    for type in type_list:
        id = int(type["url"].split("/")[-2])
        type_values.append([id, type["name"]])
    query = create_insert_query(table_name=TYPE_TABLE, rows=type_values)
    cursor.execute(query)

def init_pokemon_table(cursor):
    result = requests.get(POKEMONS_URL)
    if result.status_code != 200:
        raise HTTPException(status_code=404, detail="erorr in api")
    dto_pokemon = DtoPokemon(pokemons_object=result.json())
    values_pokemon_table = []
    values_pokemon_types_table = []
    print(f"Start read pokemons")
    for i, pokemon_object in enumerate(dto_pokemon.results):
        pokemon = get_pokemon(pokemon_object["url"])
        values_pokemon_table.append([pokemon.id,pokemon.name,pokemon.height,pokemon.weight])
        for type in pokemon.types_ids:
            values_pokemon_types_table.append([pokemon.id,type])
        print(f"read {i}, out of {len(dto_pokemon.results)}")

    query_pokemon_table = create_insert_query(table_name=POKEMON_TABLE, rows=values_pokemon_table)
    query_pokemon_type_table = create_insert_query(table_name=POKEMON_TYPE_TABLE, rows=values_pokemon_types_table)
    cursor.execute(query_pokemon_table)
    cursor.execute(query_pokemon_type_table)
    
def init_tables_from_json(cursor, json_path):
    with open(json_path) as f:
        data = json.load(f)
    trainer_exist = False
    values_trainer_table = []
    values_pokemon_trainer_table = []
    trainer_dict = dict()
    trainer_id_counter = 1
    for pokemon in data:
        pokemon_id = pokemon.get("id")
        for raw_trainer in pokemon.get("ownedBy"):
            trainer_exist = (raw_trainer.get("name"), raw_trainer.get("town")) in trainer_dict.keys()
            if not trainer_exist:
                trainer = Trainer(raw_trainer)
                trainer_dict[(trainer.name, trainer.town)] = trainer_id_counter
                values_trainer_table.append([trainer_id_counter, trainer.name, trainer.town])
                trainer_id_counter += 1

            trainer_id = trainer_dict[(raw_trainer.get("name"), raw_trainer.get("town"))]
            values_pokemon_trainer_table.append([pokemon_id, trainer_id])
                
    query_trainer_table = create_insert_query(table_name=TRAINER_TABLE, rows=values_trainer_table)
    query_pokemon_tainer_table = create_insert_query(table_name=POKEMON_TRAINER_TABLE, rows=values_pokemon_trainer_table)
    cursor.execute(query_trainer_table)
    cursor.execute(query_pokemon_tainer_table)

if __name__ == "__main__":
    run()
    