from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..schemas import contacts as schemas
from ..repository import contacts as crud
from ..settings.config import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@router.get("/contacts/", response_model=list[schemas.ContactResponse])
def read_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)

@router.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    crud.delete_contact(db, contact_id)
    return {"message": "Contact deleted"}

@router.get("/contacts/search/", response_model=list[schemas.ContactResponse])
def search_contacts(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)

@router.get("/contacts/birthdays/", response_model=list[schemas.ContactResponse])
def birthdays(db: Session = Depends(get_db)):
    return crud.get_birthdays(db)
