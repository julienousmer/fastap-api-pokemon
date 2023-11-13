from pydantic import BaseModel
from typing import List


class Pokemon(BaseModel):
    pokedex_id: int
    name: str
    size: float
    weight: float
    basic_stats: float
    image: str
    types: List[int]
    skills: List[int]


class PokemonCreate(Pokemon):
    pass


class Type(BaseModel):
    id: int
    name: str


class TypeCreate(Type):
    pass
