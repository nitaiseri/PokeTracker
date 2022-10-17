import pymysql 
import sys
import json

DB_NAME = "PokeTracker"
tables_creation_queries = ["CREATE TABLE pokemon(\
                                pokemon_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
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
                                FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),\
                                FOREIGN KEY(trainer_id) REFERENCES trainer(trainer_id)\
                            );"]

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

# def create_insert_query(table_name, vals, **kwargs):
#     return f'INSERT INTO {table_name}\
#             VALUES({"null, " if kwargs["null"] else ""}{str(vals)[1:-1]});'

def init_db_and_tables():
    create_db(DB_NAME)
    run_query(DB_NAME, tables_creation_queries)

def create_pokemon_insert_queries(data):
    insert_queries = []
    

def insert_all_json_data(json_path):
    with open(json_path) as f:
        data = json.load(f)
        queries = create_pokemon_insert_queries(data)

if __name__ == "__main__":
    # init_db_and_tables()
    insert_all_json_data("pokemons.json")
