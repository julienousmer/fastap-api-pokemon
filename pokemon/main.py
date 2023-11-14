import json

from fastapi import FastAPI, HTTPException

from databases import Database
from models import PokemonCreate, TypeCreate, SkillCreate

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
        raise HTTPException(status_code=404, detail="No Pokémons found")
    return pokemons


# Récupère les détails du pokémon précisé par :id
@app.get("/api/pokemons/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int):
    query = "SELECT * FROM Pokemon WHERE pokedex_id = :pokemon_id"
    values = {"pokemon_id": pokemon_id}
    pokemon = await database.fetch_one(query, values)
    if not pokemon:
        raise HTTPException(status_code=404, detail="The pokemon with this id was not found")
    return pokemon


# Récupère les détails du type précisé par :id
@app.get("/api/types/{type_id}")
async def get_type_by_id(type_id: int):
    query = "SELECT * FROM Type WHERE id = :type_id"
    values = {"type_id": type_id}
    type = await database.fetch_one(query, values)
    if not type:
        raise HTTPException(status_code=404, detail="No Types found")
    return type


# Récupère la liste de toutes les compétences
@app.get("/api/abilities")
async def get_abilities():
    query = "SELECT * FROM Skill"
    abilities = await database.fetch_all(query)
    if not abilities:
        raise HTTPException(status_code=404, detail="No Abilities found")
    return abilities


# Ajout d’un pokémon
@app.post("/api/pokemons")
async def add_pokemon(pokemon: PokemonCreate):
    check_query = "SELECT * FROM Pokemon WHERE pokedex_id = :pokedex_id"
    check_values = {"pokedex_id": pokemon.pokedex_id}
    check_pokemon = await database.fetch_one(check_query, check_values)
    if check_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already exists")

    for skill_id in pokemon.skills:
        check_query = "SELECT * FROM Skill WHERE id = :skill_id"
        check_values = {"skill_id": skill_id}
        check_ability = await database.fetch_one(check_query, check_values)
        if not check_ability:
            raise HTTPException(status_code=400, detail=f"Ability with ID {skill_id} not found")

    query = ("INSERT INTO Pokemon (pokedex_id, name, size, weight, basic_stats, image, types, skills) VALUES ("
             ":pokedex_id, :name, :size, :weight, :basic_stats, :image, :types, :skills)")
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


# Modification du pokémon précisé par :id
@app.put("/api/pokemons/{pokemon_id}")
async def update_pokemon(pokemon_id: int, pokemon: PokemonCreate):
    # Check if pokemon already exists
    existing_query = "SELECT * FROM Pokemon WHERE pokedex_id = :pokemon_id"
    existing_values = {"pokemon_id": pokemon_id}
    existing_pokemon = await database.fetch_one(existing_query, existing_values)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    # Check if skills exist
    for skill_id in pokemon.skills:
        check_query = "SELECT * FROM Skill WHERE id = :skill_id"
        check_values = {"skill_id": skill_id}
        check_ability = await database.fetch_one(check_query, check_values)
        if not check_ability:
            raise HTTPException(status_code=400, detail=f"Ability with ID {skill_id} not found")

    # Check if types exist
    for type_id in pokemon.types:
        check_query = "SELECT * FROM Type WHERE id = :type_id"
        check_values = {"type_id": type_id}
        check_type = await database.fetch_one(check_query, check_values)
        if not check_type:
            raise HTTPException(status_code=400, detail=f"Type with ID {type_id} not found")

    query = ("UPDATE Pokemon SET pokedex_id = :pokedex_id, name = :name, size = :size, weight = :weight, basic_stats = "
             ":basic_stats, image = :image, types = :types, skills = :skills WHERE pokedex_id = :pokemon_id")
    values = {
        "pokemon_id": pokemon_id,
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
        return {"message": "Pokemon updated !"}
    raise HTTPException(status_code=404, detail="Pokemon not found")


# Modification de la compétence précisé par :id
@app.put("/api/abilities/{ability_id}")
async def update_ability(ability_id: int, ability: SkillCreate):
    query = ("UPDATE Skill SET id = :id, name = :name, description = :description,"
             "power = :power, accuracy = :accuracy, life_max = :life_max, type_name = :type_name WHERE id = "
             ":ability_id")
    values = {
        "ability_id": ability.id,
        "id": ability.id,
        "name": ability.name,
        "description": ability.description,
        "power": ability.power,
        "accuracy": ability.accuracy,
        "life_max": ability.life_max,
        "type_name": ability.type_name,
    }

    ability = await database.execute(query, values)
    if ability:
        return {"message": "Ability updated !"}
    raise HTTPException(status_code=404, detail="Ability not found")


# Modification du type précisé par :id
@app.put("/api/type/{type_id}")
async def update_type(type_id: int, type: TypeCreate):
    query = "UPDATE Type SET id = :id, name = :name WHERE id = :type_id"
    values = {"type_id": type_id, "id": type.id, "name": type.name}

    type = await database.execute(query, values)
    if type:
        return {"message": "Type updated !"}
    raise HTTPException(status_code=404, detail="Type not found")


# Suppression du pokémon précisé par :id
@app.delete("/api/pokemon/{pokemon_id}")
async def delete_pokemon(pokemon_id: int):
    name_query = "SELECT name FROM Pokemon WHERE pokedex_id = :pokemon_id"
    name_values = {"pokemon_id": pokemon_id}
    pokemon_name = await database.fetch_val(name_query, name_values)

    if pokemon_name is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    delete_query = "DELETE FROM Pokemon WHERE pokedex_id = :pokedex_id"
    delete_values = {"pokedex_id": pokemon_id}
    await database.execute(delete_query, delete_values)

    return {"message": f"The pokemon {pokemon_name} is deleted !"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
