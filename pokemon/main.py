from fastapi import FastAPI, HTTPException
import databases
from databases import Database

app = FastAPI()

# Étape 2: Connectez-vous à la base de données SQLite en utilisant le module "databases"
database = Database("sqlite:///./db/pokemon.sqlite")


@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


# Exemple d'un point de l'API pour obtenir tous les types de Pokémon
@app.get("/types")
async def get_pokemon_types():
    query = "SELECT * FROM Type"
    types = await database.fetch_all(query)
    if not types:
        raise HTTPException(status_code=404, detail="Pas de types trouvés")
    return types


# Exemple d'un point de l'API pour obtenir un Pokémon par son ID
@app.get("/pokemon/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int):
    query = "SELECT * FROM Pokemon WHERE PokemonID = :pokemon_id"
    values = {"pokemon_id": pokemon_id}
    pokemon = await database.fetch_one(query, values)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon


# Étape 4: Exécutez l'application FastAPI
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
