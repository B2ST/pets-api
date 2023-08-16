from pydantic import BaseModel

class SpeciesBase(BaseModel):
    species: str

class SpeciesCreate(SpeciesBase):
    pass

class Species(SpeciesBase):
    id: int

    class Config:
        orm_mode = True
        