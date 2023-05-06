from fastapi import FastAPI, Depends, APIRouter, HTTPException,status
from dbs_assignment.schemas import User, PatchUser
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import User as UserModel
from datetime import datetime


router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):

    # Check na birth_date format
    try:
        datetime.strptime(user.birth_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # Je to child user?
    user_birth_date = datetime.strptime(user.birth_date, "%Y-%m-%d")
    if (datetime.now().year - user_birth_date.year) < 18:
        user.is_childuser = True
    
    if not user.name or not user.surname or not user.email or not user.birth_date or not user.personal_identificator:
        raise HTTPException(status_code=400, detail="Missing Required Information")

    # Je dospely email unikatny?
    if not user.is_childuser and db.query(UserModel).filter_by(email=user.email).filter(UserModel.is_childuser==False).first() is not None:
         raise HTTPException(status_code=409, detail="Email Already Taken")
    

    to_create = UserModel(
        id=user.id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        birth_date=user.birth_date,
        personal_identificator=user.personal_identificator,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_childuser=user.is_childuser,
    )
    db.add(to_create)
    db.commit()
    db.refresh(to_create)
    return {
        "id": to_create.id,
        "name": to_create.name,
        "surname": to_create.surname,
        "email": to_create.email,
        "birth_date": to_create.birth_date,
        "personal_identificator": to_create.personal_identificator,
        "created_at": to_create.created_at,
        "updated_at": to_create.updated_at,
    }


@router.get("/users/{id}",status_code=status.HTTP_200_OK)
async def get_by_id(id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    else:
        return {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "birth_date": user.birth_date,
            "personal_identificator": user.personal_identificator,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

@router.patch("/users/{id}",status_code=status.HTTP_200_OK)
async def patch_user(id: str, user: PatchUser, db: Session = Depends(get_db)):
    to_patch = db.query(UserModel).filter(UserModel.id == id).first()
    if not to_patch:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    if not user.is_childuser and db.query(UserModel).filter_by(email=user.email).filter(UserModel.is_childuser==False).first() is not None:
        raise HTTPException(status_code=409, detail="Email Already Taken")

    to_patch.name = user.name or to_patch.name
    to_patch.surname = user.surname or to_patch.surname
    to_patch.email = user.email or to_patch.email
    to_patch.birth_date = user.birth_date or to_patch.birth_date
    to_patch.personal_identificator = user.personal_identificator or to_patch.personal_identificator
    to_patch.updated_at = datetime.now()
    to_patch.is_childuser = user.is_childuser or to_patch.is_childuser
    db.commit()
    db.refresh(to_patch)
    return {
        "id": to_patch.id,
        "name": to_patch.name,
        "surname": to_patch.surname,
        "email": to_patch.email,
        "birth_date": to_patch.birth_date,
        "personal_identificator": to_patch.personal_identificator,
        "created_at": to_patch.created_at,
        "updated_at": to_patch.updated_at
    }
