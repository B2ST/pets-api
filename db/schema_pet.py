from pydantic import BaseModel
from typing import Optional
from . import schema_species as species

class PetBase(BaseModel):
    name: str
    age: int

class PetCreate(PetBase):
    speciesID: int

class Pet(PetBase):
    id: int
    speciesID: int
    species: Optional[species.Species]

    class Config: 
        orm_mode = True