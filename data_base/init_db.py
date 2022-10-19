import pymysql
import sys
import json

DB_NAME = "PokeTracker"
POKEMON_TABLE = "Pokemon"
TRAINER_TABLE = "Trainer"
POKEMON_TRAINER_TABLE = "Pokemon_Trainer"

tables_creation_queries = ["CREATE TABLE pokemon(\
                                pokemon_id INT NOT NULL PRIMARY KEY,\
                                name VARCHAR(20),\
                                type VARCHAR(20),\
                                height INT,\
                                weight INT\
                            );",
                           "CREATE TABLE trainer(\
                                trainer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                name VARCHAR(20),\
                                town VARCHAR(20),\
                                UNIQUE KEY full_name (name , town)\
                            );",
                           "CREATE TABLE pokemon_trainer(\
                                pokemon_id INT,\
                                trainer_id INT,\
                                PRIMARY KEY(pokemon_id , trainer_id),\
                                FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),\
                                FOREIGN KEY(trainer_id) REFERENCES trainer(trainer_id)\
                            );"]
# HELLO BAD CODE PRACTICE

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


def create_insert_query(table_name, vals, has_id):
    return f'INSERT INTO {table_name}\
            VALUES({"" if has_id else "null, "}{str(vals)[1:-1]});'


def init_db_and_tables():
    create_db(DB_NAME)
    run_query(DB_NAME, tables_creation_queries)


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
    init_db_and_tables()
    insert_all_json_data(DB_NAME, "pokemons.json")
