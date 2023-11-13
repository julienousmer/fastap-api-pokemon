import json

from fastapi import FastAPI, HTTPException

from databases import Database
from models import PokemonCreate, TypeCreate

app = FastAPI()

# Étape 2: Connectez-vous à la base de données SQLite en utilisant le module "databases"
database = Database("sqlite:///./db/pokemon.sqlite")


@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


# Récupère la liste de tous les pokémons
@app.get("/api/pokemons")
async def get_pokemons():
    query = "SELECT * FROM Pokemon"
    pokemons = await database.fetch_all(query)
    if not pokemons:
        raise HTTPException(status_code=404, detail="Pokémons not found")
    return pokemons


# Récupère les détails du pokémon précisé par :id
@app.get("/api/pokemon/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int):
    query = "SELECT * FROM Pokemon WHERE PokemonID = :pokemon_id"
    values = {"pokemon_id": pokemon_id}
    pokemon = await database.fetch_one(query, values)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon


# Récupère les détails du type précisé par :id
@app.get("/api/types/{type_id}")
async def get_type_by_id(type_id: int):
    query = "SELECT * FROM Type WHERE TypeID = :type_id"
    values = {"type_id": type_id}
    type = await database.fetch_one(query, values)
    if not type:
        raise HTTPException(status_code=404, detail="Type not found")
    return type


# Récupère la liste de toutes les compétences
@app.get("/api/abilities")
async def get_abilities():
    query = "SELECT * FROM Skill"
    abilities = await database.fetch_all(query)
    if not abilities:
        raise HTTPException(status_code=404, detail="Abilities not found")
    return abilities


# Ajout d’un pokémon
@app.post("/api/pokemon")
async def add_pokemon(pokemon: PokemonCreate):
    check_query = "SELECT * FROM Pokemon WHERE pokedex_id = :pokedex_id"
    check_values = {"pokedex_id": pokemon.pokedex_id}
    check_pokemon = await database.fetch_one(check_query, check_values)
    if check_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already exists")

    query = "INSERT INTO Pokemon (pokedex_id, name, size, weight, basic_stats, image, types, skills) VALUES (:pokedex_id, :name, :size, :weight, :basic_stats, :image, :types, :skills)"
    values = {
        "pokedex_id": pokemon.pokedex_id,
        "name": pokemon.name,
        "size": pokemon.size,
        "weight": pokemon.weight,
        "basic_stats": pokemon.basic_stats,
        "image": pokemon.image,
        "types": json.dumps(pokemon.types),
        "skills": json.dumps(pokemon.skills),
    }

    pokemon = await database.execute(query, values)
    if pokemon:
        return {"message": "Pokemon added !"}
    raise HTTPException(status_code=404, detail="Pokemon already exist")


# Ajout d’un type
@app.post("/api/types")
async def add_type(type: TypeCreate):
    check_query = "SELECT * FROM Type WHERE name = :name"
    check_values = {"name": type.name}
    check_type = await database.fetch_one(check_query, check_values)
    if check_type:
        raise HTTPException(status_code=400, detail="Type already exists")

    query = "INSERT INTO Type (name) VALUES (:name)"
    values = {"name": type.name}

    type = await database.execute(query, values)
    if type:
        return {"message": "Type added !"}
    raise HTTPException(status_code=404, detail="Type already exist")


# Étape 4: Exécutez l'application FastAPI
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
