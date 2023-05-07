from fastapi import FastAPI, Depends, APIRouter, HTTPException,status
from dbs_assignment.schemas import Reservation
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Reservation as ReservationModel
from dbs_assignment.models import Instance as InstanceModel
from dbs_assignment.models import User as UserModel
from dbs_assignment.models import Rental as RentalModel
from datetime import datetime, timedelta
from uuid import uuid4


router = APIRouter()

@router.post("/reservations/",status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: Reservation, db: Session = Depends(get_db)):
    if not reservation.id:
        reservation.id = str(uuid4())

    #check ci existuje user
    if not db.query(UserModel).filter(UserModel.id == reservation.user_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    
    # check if a publication is not available if so make reservation
    if not db.query(InstanceModel).filter(InstanceModel.publication_id == reservation.publication_id).filter(InstanceModel.status == "available").first():
        to_create = ReservationModel(
            id=reservation.id,
            user_id=reservation.user_id,
            publication_id = reservation.publication_id,
            created_at=datetime.now(),
        )
        db.add(to_create)
        db.commit()
        db.refresh(to_create)
        return {
            "id": to_create.id,
            "user_id": to_create.user_id,
            "publication_id": to_create.publication_id,
            "created_at": to_create.created_at,
        }
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@router.get("/reservations/{reservation_id}",status_code=status.HTTP_200_OK)
async def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    if not db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
        return {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "publication_id": reservation.publication_id,
            "created_at": reservation.created_at,
        }

@router.delete("/reservations/{reservation_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    if not db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
        db.delete(reservation)
        db.commit()
        return {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "publication_id": reservation.publication_id,
            "created_at": reservation.created_at,
        }
    
        
    