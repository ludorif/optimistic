from pydantic import BaseModel

class Date(BaseModel):
    event_id: str

class Event(BaseModel):
    event_id: str