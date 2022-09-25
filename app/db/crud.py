import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.db import models, schema


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = "%(asctime)s:%(name)s:%(message)s"
logging.basicConfig(filename="crud.log", format=formatter)

def get_country(db: Session, id: int):
    print(db.query(models.Record).filter(models.Record.id == id))
    return db.query(models.Record).filter(models.Record.id == id).first()

def get_country_to_be_deleted(db: Session, term: Optional[str]):
    return db.query(models.Record).filter(models.Record.country == term).first()

def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Record).offset(skip).limit(limit).all()


def create_country(db: Session, item: schema.CountryRecord):
    db_item = models.Record(**item.dict())
    # db_item = models.Record(**item)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_country(db: Session, id: int):
    db_item = get_country(db,id)
    logger.info(f"Delete Country from crud.py {db_item}")
    if not db_item:
        raise ValueError("No Such Entity")
    db.delete(db_item)
    db.commit()
    return {"ok":True}