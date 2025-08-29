#  Copyright (c) 2025 Ludovic Riffiod
from pydantic import BaseModel

class Date(BaseModel):
    selectedDate: str

class Event(BaseModel):
    event_id: str

class HealthCheck(BaseModel):
    status: str = "OK"