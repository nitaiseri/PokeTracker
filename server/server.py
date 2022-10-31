from urllib import request
from fastapi import FastAPI, HTTPException
from json import JSONDecodeError
from fastapi import Request, status, Response
from fastapi.responses import JSONResponse
from pymysql.err import IntegrityError
import uvicorn
from data_base.db_manager import db_manager
from data_base.dtos import Trainer
from server_utils import *

app = FastAPI()


@app.get('/')
def root():
    return "Server is up and running"

# Path parameter -Get pokemon by name
@app.get('/pokemons/{pokemon_name}', status_code=status.HTTP_200_OK)
def get_pokemon_by_name(pokemon_name):
    if not validate_input(pokemon_name):
        raise HTTPException(status_code=400, detail="Wrong parameter")
    pokemon_details = db_manager.get_pokemon(pokemon_name)
    return pokemon_details

# Query parameter -Get pokemon by prameters
@app.get('/pokemons', status_code=status.HTTP_200_OK)
def get_pokemons_by_parameters(type=None, trainer_name=None):
    if not validate_input(type) or not validate_input(trainer_name):
        raise HTTPException(status_code=400, detail="Wrong parameter")
    pokemons = []
    if trainer_name is not None and type is not None:
        pokemons = db_manager.get_pokemons_name_by_trainer_name_and_type(
            trainer_name, type)
    elif trainer_name is not None:
        pokemons = db_manager.get_pokemons_name_by_trainer_name(trainer_name)
    elif type is not None:
        pokemons = db_manager.get_pokemons_by_type(type)
    return pokemons

@app.post('/trainers', status_code=status.HTTP_201_CREATED)  # Add a trainer
async def add_trainer(trainer: Request, respone: Response):
    try:
        raw_new_trainer = await trainer.json()
        new_trainer = Trainer(raw_new_trainer)
        if not validate_input(new_trainer.name) or not validate_input(new_trainer.town):
            raise HTTPException(status_code=400, detail="Bad Values")
        return db_manager.add_new_trainer(new_trainer.name, new_trainer.town)
    except (JSONDecodeError, KeyError) as ex:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"name": "Some Name", "town": "Some Town"})
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Trainer already exist")

@app.get('/trainers', status_code=status.HTTP_200_OK)  # Query parameter - Get
def get_trainers_by_pokemon(pokemon_name):
    if not validate_input(pokemon_name):
        raise HTTPException(status_code=400, detail="Wrong parameter")
    trainers = db_manager.get_trainers_name_by_pokemon_name(pokemon_name)
    return trainers

# Make evolve of a spesific pokemon of a spesific trainer.
@app.patch('/pokemons/evolve', status_code=status.HTTP_200_OK)
def evolve_pokemon_by_trainer(trainer_name, pokemon_name):
    if not validate_input(pokemon_name) or not validate_input(trainer_name):
        raise HTTPException(status_code=400, detail="Wrong parameter")
    db_manager.evolve_pokemon(trainer_name, pokemon_name)


# Delete a spesific pokemon of a spesific trainer.
@app.delete('/pokemons/{pokemon_name}/trainers/{trainer_name}', status_code=status.HTTP_200_OK)
def delete_pokemon_of_trainer(pokemon_name, trainer_name):
    if not validate_input(pokemon_name) or not validate_input(trainer_name):
        raise HTTPException(status_code=400, detail="Wrong parameter")
    return db_manager.delete_pokemon_of_specific_trainer(pokemon_name, trainer_name)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
