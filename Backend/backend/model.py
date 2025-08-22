from pydantic import BaseModel

class Date(BaseModel):
    selectedDate: str

class Event(BaseModel):
    event_id: str