class DtoPokemon:
    def __init__(self, pokemons_object: dict) -> None:
        self.results = pokemons_object["results"]
        self.next_url = pokemons_object["next"]



class Pokemon:
    def __init__(self, pokemon_object) -> None:
        self.id = pokemon_object["id"]
        self.name = pokemon_object["name"]
        self.height = pokemon_object["height"]
        self.weight = pokemon_object["weight"]
        self.types_ids = [self.get_type_id_from_url(type['type']["url"]) for type in pokemon_object["types"]]

    def get_type_id_from_url(self, url):
        return int(url.split("/")[-2])
    
    def get_items(self):
        return self.id, self.name, self.height, self.weight

    def get_id(self):
        return self.id

class Trainer:
    def __init__(self, trainer_object) -> None:
        self.name = trainer_object["name"]
        self.town = trainer_object["town"]  
    
    def get_items(self):
        return self.name, self.towm