from fastapi import FastAPI, Depends, APIRouter, HTTPException,status
from dbs_assignment.schemas import Instance
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Instance as InstanceModel
from dbs_assignment.models import Publication as PublicationModel
from datetime import datetime
from uuid import uuid4


router = APIRouter()

@router.post("/instances/",status_code=status.HTTP_201_CREATED)
async def create_instance(instance: Instance, db: Session = Depends(get_db)):
    if not instance.id:
        instance.id = str(uuid4())
    
    print(instance.publication_id)
    # Check ci existuje publikacia
    if not db.query(PublicationModel).filter(PublicationModel.id == instance.publication_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    
    # check if correct status is given
    if instance.status not in ["available", "reserved"]:
        raise HTTPException(status_code=400, detail="Not Found")

    to_create = InstanceModel(
        id=instance.id,
        type=instance.type,
        publisher=instance.publisher,
        year=instance.year,
        publication_id=instance.publication_id,
        status=instance.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(to_create)
    db.commit()
    db.refresh(to_create)
    return {
        "id": to_create.id,
        "type": to_create.type,
        "publisher": to_create.publisher,
        "year": to_create.year,
        "publication_id": to_create.publication_id,
        "status": to_create.status,
        "created_at": to_create.created_at,
        "updated_at": to_create.updated_at,
    }

@router.get("/instances/{id}",status_code=status.HTTP_200_OK)
async def get_by_id(id: str, db: Session = Depends(get_db)):
    instance = db.query(InstanceModel).filter(InstanceModel.id == id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return {
            "id": instance.id,
            "type": instance.type,
            "publisher": instance.publisher,
            "year": instance.year,
            "publication_id": instance.publication_id,
            "status": instance.status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
    