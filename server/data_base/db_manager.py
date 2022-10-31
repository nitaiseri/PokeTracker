import pymysql
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
        if not validate_type(self.connection, type):
            raise HTTPException(status_code=400, detail="No such type")
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_POKEMON_BY_TYPE.format(type_=type))
            return cursor.fetchall()

    def get_trainers_name_by_pokemon_name(self, pokemon_name):
        if not validate_pokemon_name(self.connection, pokemon_name):
            raise HTTPException(status_code=400, detail="No such Pokemon")
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_TRAINERS_BY_POKEMON.format(pokemon_name=pokemon_name))
            return cursor.fetchall()
    
    def get_pokemons_name_by_trainer_name(self, trainer_name):
        if not validate_trainer_name(self.connection, trainer_name):
            raise HTTPException(status_code=400, detail="No such trainer")
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_POKEMONS_BY_TRAINER.format(trainer_name=trainer_name))
            return cursor.fetchall()
    
    def get_pokemons_name_by_trainer_name_and_type(self, trainer_name, type):
        if not validate_trainer_name(self.connection, trainer_name) or\
            not validate_type(self.connection, type):
            raise HTTPException(status_code=400, detail="No such trainer or type")
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_POKEMONS_BY_TRAINER_AND_TYPE.format(trainer_name=trainer_name, type=type))
            return cursor.fetchall()
        
    def get_most_owned_pokemon(self):
        with self.connection.cursor() as cursor:
            cursor.execute(CREATE_VIEW_OF_NUMS_OWNED_POKEMONS)
            cursor.execute(SELECT_MOST_OWNED_POKEMON)
            return cursor.fetchall() 
    
    def get_pokemon(self, pokemon_name):
        if not validate_pokemon_name(self.connection, pokemon_name):
            raise HTTPException(status_code=400, detail="No such Pokemon")
        with self.connection.cursor() as cursor:
            cursor.execute(GET_POKEMON.format(name=pokemon_name))
            return cursor.fetchall() 

    def add_new_trainer(self, name, town):
        new_id = self.get_new_trainer_id()
        with self.connection.cursor() as cursor:
                trainer_values = [new_id, name, town]
                cursor.execute(create_insert_query(TRAINER_TABLE, [trainer_values]))
                new_trainer = {"id": new_id, "name": name, "town": town}
                self.connection.commit()
                return new_trainer

    def get_new_trainer_id(self):
        all_ids = None
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_MAX_TRAINER_ID)
            return cursor.fetchone()["max_id"] + 1
    
    def delete_pokemon_of_specific_trainer(self, pokemon_name, trainer_name):
        if not validate_trainer_name(self.connection, trainer_name) or not validate_pokemon_name(self.connection, pokemon_name):
            raise HTTPException(status_code=400, detail="No such trainer or pokemon")
        with self.connection.cursor() as cursor:
            return_value = cursor.execute(DELETE_POKEMON_OF_TRAINER.format(pokemon_name=pokemon_name, trainer_name=trainer_name))
            if return_value:
                self.connection.commit()
                return return_value
            raise HTTPException(status_code=400, detail="This trainer does not own this pokemon.")

    
    def evolve_pokemon(self, trainer, pokemon):
        trainer_id = validate_trainer_name(self.connection, trainer)
        pokemon_id = validate_pokemon_name(self.connection, pokemon)
        if not trainer_id or not pokemon_id:
            raise HTTPException(status_code=400, detail="No such trainer or pokemon")
        if not validate_ownership(self.connection, trainer_id, pokemon_id):
            raise HTTPException(status_code=400, detail=f"{trainer} does not own {pokemon}.")
        new_pokemon_id = get_pokemon_next_generation_id(pokemon_id)
        if pokemon_id == new_pokemon_id:
            raise HTTPException(status_code=400, detail=f"{pokemon} cannot evolve. He is already the best version of itself.")
        with self.connection.cursor() as cursor:
            cursor.execute(UPDATE_POKEMON_ID_IN_ONERSHIP.format(new_id=new_pokemon_id, old_id=pokemon_id, trainer_id=trainer_id))
        self.connection.commit()
        
db_manager = DB_Manager()
