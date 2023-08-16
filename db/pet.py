from sqlalchemy.orm import Session, Query
from sqlalchemy import select
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

from . import model_pet, model_species, schema_pet as schemas

class PetsFilter(Filter):
    name: Optional[str]
    age: Optional[int]
    species: Optional[str]
    class Constants(Filter.Constants):
        model = model_pet.Pet

def get_pet(db: Session, pet_id: int):
    return db.query(model_pet.Pet).filter(model_pet.Pet.id == pet_id).first()

def list_pets(db: Session, filter: PetsFilter ):
    # get list of species
    species = db.execute(select(model_species.Species.species)).scalars().all()

    # filter pets by species
    if filter.species in species:
       for idx, s in enumerate(species, 1):
           if filter.species == s:
              filteredSpecies = db.execute(select(model_pet.Pet).filter(model_pet.Pet.speciesID == idx))
              return filteredSpecies.scalars().all()
           
    elif filter.species != None and filter.species not in species:
       return []

    # if not filtering by species, use PetsFilter approach
    filter.species = None
    query = filter.filter(select(model_pet.Pet)).join(model_species.Species)
    res = db.execute(query)

    return res.scalars().all()

def create_pet(db: Session, pet: schemas.PetCreate):
    db_pet = model_pet.Pet(speciesID=pet.speciesID, age=pet.age, name=pet.name)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet
