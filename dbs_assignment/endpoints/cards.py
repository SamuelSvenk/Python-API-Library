from fastapi import FastAPI, Depends, APIRouter, HTTPException, Response,status
from dbs_assignment.schemas import Card, PatchCard
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Card as CardModel
from datetime import datetime
from uuid import uuid4

router = APIRouter()

@router.post("/cards/",status_code=status.HTTP_201_CREATED)
async def create_card(card: Card, db: Session = Depends(get_db)):
    if not card.id:
        card.id = str(uuid4())
        
    to_create = CardModel(
        id=card.id,
        user_id=card.user_id,
        magstripe=card.magstripe,
        status=card.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(to_create)
    db.commit()
    db.refresh(to_create)
    return {
        "id": to_create.id,
        "user_id": to_create.user_id,
        "magstripe": to_create.magstripe,
        "status": to_create.status,
        "created_at": to_create.created_at,
        "updated_at": to_create.updated_at,
    }

@router.get("/cards/{id}",status_code=status.HTTP_200_OK)
async def get_by_id(id: str, db: Session = Depends(get_db)):
    card = db.query(CardModel).filter(CardModel.id == id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return {
            "id": card.id,
            "user_id": card.user_id,
            "magstripe": card.magstripe,
            "status": card.status,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
    }

@router.patch("/cards/{id}",status_code=status.HTTP_200_OK)
async def patch_card(id: str, card: PatchCard, db: Session = Depends(get_db)):
    if not db.query(CardModel).filter(CardModel.id == id).first():
        raise HTTPException(status_code=404, detail="Not Found")

    if card.status not in ["active", "inactive", "expired"]:
        raise HTTPException(status_code=400, detail="Bad Request")

    to_patch = db.query(CardModel).filter(CardModel.id == id).first()
    to_patch.magstripe = card.magstripe or to_patch.magstripe
    to_patch.status = card.status or to_patch.status
    to_patch.updated_at = datetime.now()
    db.commit()
    db.refresh(to_patch)
    return {
        "id": to_patch.id,
        "user_id": to_patch.user_id,
        "magstripe": to_patch.magstripe,
        "status": to_patch.status,
        "created_at": to_patch.created_at,
        "updated_at": to_patch.updated_at,
    }

@router.delete("/cards/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(id: str, db: Session = Depends(get_db)):
    to_delete = db.query(CardModel).filter(CardModel.id == id).first()
    db.delete(to_delete)
    db.commit()
    return 