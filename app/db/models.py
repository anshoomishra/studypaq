from dataclasses import Field
from enum import auto
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .sessions import Base


class Record(Base):
    __tablename__ = "Country_Table"

    id = Column(Integer, primary_key=True, index=True)
    
    country = Column(String(255))

    def __str__(self) -> str:
        return self.country
    