#  Copyright (c) 2025 Ludovic Riffiod
from pydantic import BaseModel

class Date(BaseModel):
    selectedDate: str

class ExistingEvent(BaseModel):
    event_id: int
    uuid: str
    planet_id: int

class NewEvent(BaseModel):
    story: str
    event_date: str
    uuid: str
    planet_id: int

class HealthCheck(BaseModel):
    status: str = "OK"

class Planet(BaseModel):
    name: str
    type: str
    first_story: str