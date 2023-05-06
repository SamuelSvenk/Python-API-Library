from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from dbs_assignment.schemas import Author, PatchAuthor
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Author as AuthorModel
from datetime import datetime
from uuid import uuid4

router = APIRouter()

@router.post("/authors/",status_code=status.HTTP_201_CREATED)
async def create_author(author: Author, db: Session = Depends(get_db)):
    if not author.id:
        author.id = str(uuid4())

        # Check na kominaciu mena a priezviska
    if db.query(AuthorModel).filter(AuthorModel.name == author.name).filter(AuthorModel.surname == author.surname).first():
        raise HTTPException(status_code=409, detail="Conflict")
        
    to_create = AuthorModel(
        id=author.id,
        name=author.name,
        surname=author.surname,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(to_create)
    db.commit()
    db.refresh(to_create)
    return {
        "id": to_create.id,
        "name": to_create.name,
        "surname": to_create.surname,
        "created_at": to_create.created_at,
        "updated_at": to_create.updated_at,
    }

@router.get("/authors/{id}",status_code=status.HTTP_200_OK)
async def get_by_id(id: str, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return {
            "id": author.id,
            "name": author.name,
            "surname": author.surname,
            "created_at": author.created_at,
            "updated_at": author.updated_at,
    }

@router.patch("/authors/{id}",status_code=status.HTTP_200_OK)
async def patch_author(id: str, author: PatchAuthor, db: Session = Depends(get_db)):
    if not db.query(AuthorModel).filter(AuthorModel.id == id).first():
        raise HTTPException(status_code=404, detail="Not Found")

    to_patch = db.query(AuthorModel).filter(AuthorModel.id == id).first()
    to_patch.name = author.name or to_patch.name
    to_patch.surname = author.surname or to_patch.surname
    to_patch.updated_at = datetime.now()
    db.commit()
    db.refresh(to_patch)
    return {
        "id": to_patch.id,
        "name": to_patch.name,
        "surname": to_patch.surname,
        "created_at": to_patch.created_at,
        "updated_at": to_patch.updated_at,
    }

@router.delete("/authors/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(id: str, db: Session = Depends(get_db)):
    if not db.query(AuthorModel).filter(AuthorModel.id == id).first():
        raise HTTPException(status_code=404, detail="Not Found")

    to_delete = db.query(AuthorModel).filter(AuthorModel.id == id).first()
    db.delete(to_delete)
    db.commit()
    return 
