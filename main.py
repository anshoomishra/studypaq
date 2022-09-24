import logging
from importlib.resources import path
from pyexpat import model
from re import ASCII
from statistics import mode
from tempfile import template
from fastapi import FastAPI,Depends,HTTPException,Request
import dotenv
from fastapi.responses import HTMLResponse
import os
from functools import lru_cache
import settings
from typing import List,Optional
from db import crud
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

import pathlib

logging.basicConfig(filename='file.log',level=logging.DEBUG,format="%(asctime)s:%(name)s:%(message)s")

logger.debug("Debug")

app = FastAPI()
# print(settings.development.DEBUG)
app.mount("/static", StaticFiles(directory="static"), name="static")
settings = settings.get_settings

logger.info("Started")

BASEDIR  = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory= str(BASEDIR / "templates"))

from db import  models, schema
from db.sessions import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/",response_class=HTMLResponse)
def info(request:Request):
   
    return templates.TemplateResponse("home.html",{"request":request})

@app.get("/countries/", response_model=List[schema.CountryRecord])
def read_country(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries =  crud.get_countries(db, skip=skip, limit=limit)
    return countries


@app.get("/search/")
def auto_complate_countries(term:Optional[str],db:Session = Depends(get_db)):
    countries = db.query(models.Record).filter(models.Record.country.contains(term)).all()
    suggestions = []
    for item in countries:
        suggestions.append(item.country)
    
    return suggestions
result = []
file = "db/db.txt"
_file = pathlib.Path(__file__).parent.resolve()

file_path = _file / file

with open(str(file_path),encoding="utf-8") as file:
    for item in file:
        result.append(" ".join(item.split()))

def create_bulk_country(cr: schema.CountryRecord, db: Session = Depends(get_db)):
    print(cr)
    db_country = None
    try:
        db_country = crud.get_country(db, id=cr.id)
    except:
        pass

    print(db_country)
    if db_country:
        raise HTTPException(status_code=400, detail="already registered")
    return crud.create_country( item=cr,db=db)

@app.post("/countries/", response_model=schema.CountryRecord)
def create_country(cr: schema.CountryRecord, db: Session = Depends(get_db)):
    db_country = crud.get_country(db, id=cr.id)
    print(db_country)
    if db_country:
        raise HTTPException(status_code=400, detail="already registered")
    create_data(db)
    return crud.create_country(db=db, item=cr)

@app.delete("/country/delete/{term}")
def delete_country(term:Optional[str],db:Session = Depends(get_db)):
    deleted_record = None
    try:
        deleted_record =  crud.delete_country(term=term,db=db)
    except :
        return {f"{id}":"Does Not exist"}
    return deleted_record

def create_data(db):
    id = 20
    for item in result:
        cr = schema.CountryRecord(id=id,country=item)
        create_bulk_country(cr,db)
        id+=1


