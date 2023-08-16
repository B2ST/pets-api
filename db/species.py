from sqlalchemy.orm import Session

from . import model_species as models, schema_species as schemas

def get_species(db: Session, species_id: int):
    return db.query(models.Species).filter(models.Species.id == species_id).first()

def create_species(db: Session, species: schemas.SpeciesCreate):
    db_species = models.Species(species=species.species)
    db.add(db_species)
    db.commit()
    db.refresh(db_species)
    return db_species
