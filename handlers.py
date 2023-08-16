from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_filter import FilterDepends

from db import (
    pet as p, species as sp, model_pet, model_species, 
    schema_pet, schema_species, db
)

#Dependency
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

app = FastAPI()

@app.get("/pets/{pet_id}", response_model=schema_pet.Pet)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = p.get_pet(db, pet_id=pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="pet not found")
    return pet

@app.get("/pets/", response_model=list[schema_pet.Pet])
def list_pets(pets_filter: p.PetsFilter = FilterDepends(p.PetsFilter), db: Session = Depends(get_db)):
    return p.list_pets(db, filter=pets_filter)

@app.post("/pets/", response_model=schema_pet.Pet)
def create_pet(pet: schema_pet.PetCreate, db: Session = Depends(get_db)):
    return p.create_pet(db=db, pet=pet)

@app.get("/species/{species_id}", response_model=schema_species.Species)
def get_species(species_id: int, db: Session = Depends(get_db)):
    species = sp.get_species(db, species_id=species_id)
    if species is None:
        raise HTTPException(status_code=404, detail="species not found")
    return species

@app.get("/species/", response_model=list[schema_species.Species])
def list_species(db: Session = Depends(get_db)):
    return db.execute(select(model_species.Species)).scalars().all()

@app.post("/species/", response_model=schema_species.Species)
def create_species(species: schema_species.SpeciesCreate, db: Session = Depends(get_db)):
    return sp.create_species(db=db, species=species)