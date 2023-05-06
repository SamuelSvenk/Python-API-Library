from fastapi import FastAPI, Depends, APIRouter, HTTPException, Response
from dbs_assignment.schemas import Card, PatchCard
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Card as CardModel
from datetime import datetime
from uuid import uuid4

router = APIRouter()

@router.post("/cards/")
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
    return Response(status_code=201, content="Created")

@router.get("/cards/{id}")
async def get_by_id(id: str, db: Session = Depends(get_db)):
    card = db.query(CardModel).filter(CardModel.id == id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return db.query(CardModel).filter(CardModel.id == id).first()

@router.patch("/cards/{id}")
async def patch_card(id: str, card: PatchCard, db: Session = Depends(get_db)):
    if not db.query(CardModel).filter(CardModel.id == id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    


    to_patch = db.query(CardModel).filter(CardModel.id == id).first()
    to_patch.status = card.status
    to_patch.updated_at = datetime.now()
    db.commit()
    db.refresh(to_patch)
    return Response(status_code=200, content="OK")

@router.delete("/cards/{id}")
async def delete_card(id: str, db: Session = Depends(get_db)):
    to_delete = db.query(CardModel).filter(CardModel.id == id).first()
    db.delete(to_delete)
    db.commit()
    return to_delete