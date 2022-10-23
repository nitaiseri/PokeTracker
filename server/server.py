from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import requests

app = FastAPI()

@app.get('/')
def root():
    return "Server is up and running"

@app.get('/pokemons/{pokemon_name}', status_code=status.HTTP_200_OK) # Path parameter -Get pokemon by name
def get_pokemon_by_name(pokemon_name):
    pass

@app.get('/pokemons/', status_code=status.HTTP_200_OK) # Query parameter -Get pokemon by prameters
def get_pokemons_by_parameters(type=None, trainer=None):
    a=1
    pass
                 
@app.post('/trainers/', status_code=status.HTTP_200_OK) # Add a trainer
def add_trainer(trainer:Request, respone:Response):
    pass

@app.get('/trainers/', status_code=status.HTTP_200_OK) # Query parameter - Get 
def get_trainers_by_pokemon(pokemon_name):
    pass

@app.patch('/pokemons/evolve/', status_code=status.HTTP_200_OK)  # Make evolve of a spesific pokemon of a spesific trainer.
def evolve_pokemon_by_trainer(trainer, pokemon):
    pass

@app.delete('/pokemons/{pokemon_name}/trainers/{trainer_name}', status_code=status.HTTP_200_OK)  # Delete a spesific pokemon of a spesific trainer.
def delete_pokemon_of_trainer(pokemon_name):
    pass

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000,reload=True)

