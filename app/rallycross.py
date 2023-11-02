from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Model voor de rallycross driver
class RallyDriver(BaseModel):
    name: str
    country: str
    team: str

# Endpoint om alle rallycross drivers op te halen
@app.get("/drivers/", response_model=List[RallyDriver])
def get_all_drivers():
    conn = sqlite3.connect('rallycross.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, country, team FROM drivers')
    drivers = cursor.fetchall()
    conn.close()
    
    return drivers

# Endpoint om een specifieke rallycross driver op te halen op basis van naam
@app.get("/drivers/{driver_name}", response_model=RallyDriver)
def get_specific_driver(driver_name: str):
    conn = sqlite3.connect('rallycross.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, country, team FROM drivers WHERE name = ?', (driver_name,))
    driver = cursor.fetchone()
    conn.close()
    
    if driver:
        return driver
    else:
        raise HTTPException(status_code=404, detail="Driver not found")

# Endpoint om een nieuwe rallycross driver toe te voegen
@app.post("/drivers/")
def add_driver(driver: RallyDriver):
    conn = sqlite3.connect('rallycross.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO drivers (name, country, team) VALUES (?, ?, ?)', (driver.name, driver.country, driver.team))
    conn.commit()
    conn.close()
    return {"message": "Driver added successfully"}

# Endpoint om een rallycross driver te verwijderen op basis van naam
@app.delete("/drivers/{driver_name}")
def delete_driver(driver_name: str):
    conn = sqlite3.connect('rallycross.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM drivers WHERE name = ?', (driver_name,))
    conn.commit()
    conn.close()
    return {"message": "Driver deleted successfully"}