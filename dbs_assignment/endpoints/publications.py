from fastapi import FastAPI, Depends, APIRouter, HTTPException,status
from dbs_assignment.schemas import Publication
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Publication as PublicationModel
from dbs_assignment.models import Author as AuthorModel
from dbs_assignment.models import Category as CategoryModel
from datetime import datetime
from uuid import uuid4


router = APIRouter()

@router.post("/publications/",status_code=status.HTTP_201_CREATED)
async def create_publication(publication: Publication, db: Session = Depends(get_db)):
    # Create a new publication model
    new_publication = PublicationModel(
        id=uuid4(),
        title=publication.title,
        authors=[],
        categories=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add existing authors to the publication
    for author in publication.authors:
        existing_author = db.query(AuthorModel).filter(AuthorModel.name == author["name"], AuthorModel.surname == author["surname"]).first()
        if existing_author is None:
            raise HTTPException(status_code=404, detail="Not Found")
        else:
            new_publication.authors.append(existing_author)
    
    # Add existing categories to the publication
    for category in publication.categories:
        existing_category = db.query(CategoryModel).filter(CategoryModel.name == category).first()
        if existing_category is None:
            raise HTTPException(status_code=404, detail="Not Found")
        else:
            new_publication.categories.append(existing_category)

    db.add(new_publication)
    db.commit()
    db.refresh(new_publication)
    return {
        "id": new_publication.id,
        "title": new_publication.title,
        "authors": new_publication.authors,
        "categories": new_publication.categories,
        "created_at": new_publication.created_at,
        "updated_at": new_publication.updated_at,
    }

@router.get("/publications/{id}",status_code=status.HTTP_200_OK)
async def get_by_id(id: str, db: Session = Depends(get_db)):
    publication = db.query(PublicationModel).filter(PublicationModel.id == id).first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return {
            "id": publication.id,
            "title": publication.title,
            "authors": publication.authors,
            "categories": publication.categories,
            "created_at": publication.created_at,
            "updated_at": publication.updated_at,
    }
    