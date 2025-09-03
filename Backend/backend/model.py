#  Copyright (c) 2025 Ludovic Riffiod
from pydantic import BaseModel

class Date(BaseModel):
    selectedDate: str

class ExistingEvent(BaseModel):
    event_id: str
    uuid: str

class NewEvent(BaseModel):
    story: str
    event_date: str
    uuid: str

class HealthCheck(BaseModel):
    status: str = "OK"