from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from .db import Base
from . import model_species as sp

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True) 
    speciesID = Column(Integer, ForeignKey("species.id"))
    name = Column(String)
    age = Column(Integer)
    species: Mapped[sp.Species] = relationship(sp.Species, backref="pets")