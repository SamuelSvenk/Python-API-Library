from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from dbs_assignment.schemas import Category, PatchCategory
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Category as CategoryModel
from datetime import datetime
from uuid import uuid4

router = APIRouter()


@router.post("/categories/", status_code=status.HTTP_201_CREATED)
async def create_category(category: Category, db: Session = Depends(get_db)):

    if not category.id:
        category.id = str(uuid4())


    if db.query(CategoryModel).filter(CategoryModel.name == category.name).first():
        raise HTTPException(status_code=409, detail="Conflict")
    
  
    to_create = CategoryModel(
        id=category.id,
        name=category.name,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(to_create)
    db.commit()
    db.refresh(to_create)
    return {
        "id": to_create.id,
        "name": to_create.name,
        "created_at": to_create.created_at,
        "updated_at": to_create.updated_at,
    }


@router.get("/categories/{id}", status_code=status.HTTP_200_OK)
async def get_by_id(id: str, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return {
            "id": category.id,
            "name": category.name,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }


@router.patch("/categories/{id}", status_code=status.HTTP_200_OK)
async def patch_category(id: str, category: PatchCategory, db: Session = Depends(get_db)):
    if not db.query(CategoryModel).filter(CategoryModel.id == id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    
    # Check ci uz mame categoriu s tymto menom
    if db.query(CategoryModel).filter(CategoryModel.name == category.name).first():
        raise HTTPException(status_code=409, detail="Conflict")
    

    to_patch = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    to_patch.name = category.name or to_patch.name
    to_patch.updated_at = datetime.now()
    db.commit()
    db.refresh(to_patch)
    return {
        "id": to_patch.id,
        "name": to_patch.name,
        "created_at": to_patch.created_at,
        "updated_at": to_patch.updated_at,
    }


@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: str, db: Session = Depends(get_db)):
    if not db.query(CategoryModel).filter(CategoryModel.id == id).first():
        raise HTTPException(status_code=404, detail="Not Found")

    to_delete = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    db.delete(to_delete)
    db.commit()
    return 