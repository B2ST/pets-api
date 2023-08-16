from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from .db import Base


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String)
