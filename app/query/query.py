from sqlalchemy.orm import Session
from ..db import models

def query_set(db:Session):
    return db.query(models.Record)

