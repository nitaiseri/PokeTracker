import pymysql
import os
from data_base.constants.consts import *
from data_base.constants.queries import *
from data_base.db_utils import *

class DB_Manager:
    def __init__(self):
        self.connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PWD,
            db=DB,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_heaviest_pokemon(self):
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_HEAVIEST_POKEMON)
            return cursor.fetchall()
    
    def get_pokemons_by_type(self, type):
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_POKEMON_BY_TYPE.format(type_=type))
            return cursor.fetchall()

    def get_trainers_name_by_pokemon_name(self, pokemon_name):
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_TRAINERS_BY_POKEMON.format(pokemon_name=pokemon_name))
            return cursor.fetchall()
    
    def get_pokemons_name_by_trainer_name(self, trainer_name):
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_POKEMONS_BY_TRAINER.format(trainer_name=trainer_name))
            return cursor.fetchall() 
        
    def get_most_owned_pokemon(self):
        with self.connection.cursor() as cursor:
            cursor.execute(CREATE_VIEW_OF_NUMS_OWNED_POKEMONS)
            cursor.execute(SELECT_MOST_OWNED_POKEMON)
            return cursor.fetchall() 
    
    def get_pokemon(self, pokemon_name):
        with self.connection.cursor() as cursor:
            cursor.execute(GET_POKEMON.format(name=pokemon_name))
            return cursor.fetchall() 

    def add_new_trainer(self, name, town):
        new_id = self.get_new_trainer_id()
        with self.connection.cursor() as cursor:
                trainer_values = [new_id, name, town]
                cursor.execute(create_insert_query(TRAINER_TABLE, [trainer_values]))
                return cursor.fetchall() 

    def get_new_trainer_id(self):
        all_ids = None
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_MAX_TRAINER_ID)
            return cursor.fetchone()["max_id"] + 1


db_manager = DB_Manager()
print(db_manager.get_new_trainer_id())