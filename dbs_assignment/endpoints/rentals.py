from fastapi import FastAPI, Depends, APIRouter, HTTPException,status
from dbs_assignment.schemas import Rental
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import Rental as RentalModel
from dbs_assignment.models import Instance as InstanceModel
from dbs_assignment.models import Reservation as RenservationModel
from dbs_assignment.models import User as UserModel
from datetime import datetime, timedelta
from uuid import uuid4


router = APIRouter()

@router.post("/rentals/",status_code=status.HTTP_201_CREATED)
async def create_rental(rental: Rental, db: Session = Depends(get_db)):
    if not rental.id:
        rental.id = str(uuid4())

    #check ci existuje user
    if not db.query(UserModel).filter(UserModel.id == rental.user_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    
    # check ci je dlzka pouzicky vacsia ako 14 dni
    if rental.duration > 14 or rental.duration < 1:
        raise HTTPException(status_code=400, detail="Bad Request")

    #check ci existuje instance
    if not db.query(InstanceModel).filter(InstanceModel.publication_id == rental.publication_id).filter(InstanceModel.status == "available").first():
        if db.query(RenservationModel).filter(RenservationModel.publication_id == rental.publication_id).first():
            reservation = db.query(RenservationModel).filter(RenservationModel.publication_id == rental.publication_id).order_by(RenservationModel.created_at).first()
            if reservation.user_id == rental.user_id:
                instance_id = db.query(InstanceModel).filter(InstanceModel.publication_id == rental.publication_id).filter(InstanceModel.status == "available").first().id
                to_create = RentalModel(
                    id=rental.id,
                    user_id=reservation.user_id,
                    duration=reservation.duration,
                    status="active",
                    publication_id = reservation.publication_id,
                    instance_id = instance_id,
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=reservation.duration)
                )
                db.add(to_create)
                db.commit()
                db.refresh(to_create)
                return {
                    "id": to_create.id,
                    "user_id": to_create.user_id,
                    "duration": to_create.duration,
                    "status": to_create.status,
                    "publication_instance_id": to_create.instance_id,
                    "start_date": to_create.start_date,
                    "end_date": to_create.end_date
                }
            else:
                raise HTTPException(status_code=400, detail="Not Found")
        else:
            raise HTTPException(status_code=400, detail="Not Found")
    else:
        instance_id = db.query(InstanceModel).filter(InstanceModel.publication_id == rental.publication_id).filter(InstanceModel.status == "available").first().id
        to_create = RentalModel(
            id=rental.id,
            user_id=rental.user_id,
            duration=rental.duration,
            status="active",
            publication_id = rental.publication_id,
            instance_id = instance_id,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=rental.duration)
        )
        db.add(to_create)
        db.commit()
        db.refresh(to_create)
        return {
            "id": to_create.id,
            "user_id": to_create.user_id,
            "duration": to_create.duration,
            "status": to_create.status,
            "publication_instance_id": to_create.instance_id,
            "start_date": to_create.start_date,
            "end_date": to_create.end_date
        }
    
@router.get("/rentals/{rental_id}",status_code=status.HTTP_200_OK)
async def get_rental(rental_id: str, db: Session = Depends(get_db)):
    if not db.query(RentalModel).filter(RentalModel.id == rental_id).first():
        raise HTTPException(status_code=404, detail="Not Found")
    
    rental = db.query(RentalModel).filter(RentalModel.id == rental_id).first()
    return {
        "id": rental.id,
        "user_id": rental.user_id,
        "duration": rental.duration,
        "status": rental.status,
        "publication_instance_id": rental.instance_id,
        "start_date": rental.start_date,
        "end_date": rental.end_date
    }