from fastapi import FastAPI
from fastapi import Request, status, Response
import uvicorn
from data_base.db_manager import db_manager
from data_base.dtos import Trainer

app = FastAPI()


@app.get('/')
def root():
    return "Server is up and running"


# Path parameter -Get pokemon by name
@app.get('/pokemons/{pokemon_name}', status_code=status.HTTP_200_OK)
def get_pokemon_by_name(pokemon_name):
    pokemon_details = db_manager.get_pokemon(pokemon_name)
    return pokemon_details

# TODO: Wrong parameter should raise error or return empty list.


# Query parameter -Get pokemon by prameters
@app.get('/pokemons/', status_code=status.HTTP_200_OK)
def get_pokemons_by_parameters(type=None, trainer_name=None):
    pokemons = []
    if trainer_name is not None and type is not None:
        pass
    if trainer_name is not None:
        pokemons = db_manager.get_pokemons_name_by_trainer_name(trainer_name)
    elif type is not None:
        pokemons = db_manager.get_pokemons_by_type(type)
    return pokemons


@app.post('/trainers', status_code=status.HTTP_200_OK)  # Add a trainer
async def add_trainer(trainer: Request, respone: Response):
    raw_new_trainer = await trainer.json()
    try:
        new_trainer = Trainer(raw_new_trainer)
        return db_manager.add_new_trainer(new_trainer.name, new_trainer.town)
    except:

        pass


@app.get('/trainers/', status_code=status.HTTP_200_OK)  # Query parameter - Get
def get_trainers_by_pokemon(pokemon_name):
    trainers = db_manager.get_trainers_name_by_pokemon_name(pokemon_name)
    return trainers


# Make evolve of a spesific pokemon of a spesific trainer.
@app.patch('/pokemons/evolve/', status_code=status.HTTP_200_OK)
def evolve_pokemon_by_trainer(trainer, pokemon):
    pass


# Delete a spesific pokemon of a spesific trainer.
@app.delete('/pokemons/{pokemon_name}/trainers/{trainer_name}', status_code=status.HTTP_200_OK)
def delete_pokemon_of_trainer(pokemon_name):
    pass


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
