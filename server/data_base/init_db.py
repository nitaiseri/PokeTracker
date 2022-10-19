from constants.consts import *
from constants.queries import *
from unicodedata import name
import pymysql
import sys
import json
import requests
import os

from fastapi import HTTPException
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


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


def run_query(data_base, queries):
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db=data_base,
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


def create_insert_query(table_name, values, has_id):
    return f'INSERT INTO {table_name}\
            VALUES({"" if has_id else "null, "}{str(values)[1:-1]});'


def init_db():
    # create_db(DB_NAME)
    run_query(DB_NAME, tables_creation_queries)


def init_type_table(cursor):
    result = requests.get(TYPES_URL)
    data = result.json()
    if result.status_code == 200:
        type_list = data["results"]
        type_values = list(map(lambda type: type["name"], type_list))
        query = create_insert_query(
            table_name=TYPE_TABLE, values=type_values, has_id=False)

        cursor.execute(query)
    else:
        raise HTTPException(status_code=404, detail="erorr in api")


def init_pokemon_table():
    pass


def init_trainer_table():
    pass


def insert_data_to_tables():
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
            init_pokemon_table()  # Init pokemon and pokemon-type tables
            init_trainer_table()  # Init trainer and pokemon-trainer tables
        connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)


def get_pokemon_values(pokemon_object):
    return [pokemon_object["id"], pokemon_object["name"], pokemon_object["type"], pokemon_object["height"], pokemon_object["weight"]]


def insert_to_table(pokemon_object, cursor):
    poke_values = get_pokemon_values(pokemon_object)
    query = create_insert_query(POKEMON_TABLE, poke_values, True)
    cursor.execute(query)
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


def insert_all_json_data(data_base, json_path):
    with open(json_path) as f:
        data = json.load(f)
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db=data_base,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            for pokemon in data:
                insert_to_table(pokemon, cursor)
            connection.commit()
    except pymysql.Error as e:
        print(e.args[1], file=sys.stderr)


if __name__ == "__main__":
    init_db()
    insert_data_to_tables()
    # insert_all_json_data(DB_NAME, "pokemons.json")
