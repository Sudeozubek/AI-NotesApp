from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str
    description: str | None = None

class NoteResponse(NoteCreate):
    id: int

    class Config:
        from_attributes = True
