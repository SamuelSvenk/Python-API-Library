from fastapi import FastAPI, Depends, APIRouter, HTTPException,status
from dbs_assignment.schemas import Rental
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Rental as RentalModel
from dbs_assignment.models import Instance as InstanceModel
from dbs_assignment.models import Reservation as RenservationModel
from dbs_assignment.models import User as UserModel
from datetime import datetime
from uuid import uuid4


router = APIRouter()

@router.post("/rentals/",status_code=status.HTTP_201_CREATED)
async def create_rental(rental: Rental, db: Session = Depends(get_db)):
    if not rental.id:
        rental.id = str(uuid4())

    #check ci existuje user
    if not db.query(UserModel).filter(UserModel.id == rental.user_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    
    #check ci existuje instance
    if not db.query(InstanceModel).filter(InstanceModel.publication_id == rental.publication_id).filter(InstanceModel.status == "available").first():
        if db.query(RenservationModel).filter(RenservationModel.publication_id == rental.publication_id).first():
            reservation = db.query(RenservationModel).filter(RenservationModel.publication_id == rental.publication_id).order_by(RenservationModel.created_at).first()
            if reservation.user_id == rental.user_id:
                to_create = RentalModel(
                    id=rental.id,
                    user_id=reservation.user_id,
                    duration=reservation.duration,
                    publication_id=reservation.publication_id,
                    start_date=datetime.now(),
                    end_date=datetime.now()
                )
                db.add(to_create)
                db.commit()
                db.refresh(to_create)
                return {
                    "id": to_create.id,
                    "user_id": to_create.user_id,
                    "duration": to_create.duration,
                    "publication_id": to_create.publication_id,
                    "start_date": to_create.start_date,
                    "end_date": to_create.end_date
                }
            else:
                raise HTTPException(status_code=400, detail="Not Found")
        else:
            raise HTTPException(status_code=400, detail="Not Found")
    else:
        to_create = RentalModel(
            id=rental.id,
            user_id=rental.user_id,
            duration=rental.duration,
            publication_id=rental.publication_id,
            start_date=datetime.now(),
            end_date=datetime.now()
        )
        db.add(to_create)
        db.commit()
        db.refresh(to_create)
        return {
            "id": to_create.id,
            "user_id": to_create.user_id,
            "duration": to_create.duration,
            "publication_id": to_create.publication_id,
            "start_date": to_create.start_date,
            "end_date": to_create.end_date
        }