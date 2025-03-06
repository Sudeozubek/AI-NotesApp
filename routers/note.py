 from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import Note
from schemas.notes import NoteCreate, NoteResponse

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)
@router.get("/", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return note

@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content, description=note.description)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated_note: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")

    note.title = updated_note.title
    note.content = updated_note.content
    note.description = updated_note.description
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı!")

    db.delete(note)
    db.commit()
    return {"message": f"Not {note_id} başarıyla silindi"}
