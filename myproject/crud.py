from sqlalchemy.orm import Session
import models
import schemas

from sqlalchemy.orm import Session
from . import models, schemas

def get_drivers(db: Session):
    return db.query(models.Driver).all()

def get_driver(db: Session, driver_id: int):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()

def create_driver(db: Session, driver: schemas.DriverCreate):
    db_driver = models.Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def delete_driver(db: Session, driver_id: int):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver is not None:
        db.delete(driver)
        db.commit()
        return True
    return False