
from pydantic import BaseModel


class CountryRecord(BaseModel):
    id: int
    
    country: str
    

    class Config:
        orm_mode = True