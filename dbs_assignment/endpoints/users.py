from fastapi import FastAPI, Depends, APIRouter, HTTPException, Response
from dbs_assignment.schemas import User, PatchUser
from sqlalchemy.orm import Session
from dbs_assignment.database import get_db
from dbs_assignment.models import User as UserModel
from datetime import datetime

router = APIRouter()


@router.post("/users/")
async def create_user(user: User, db: Session = Depends(get_db)):
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
    return Response(status_code=201, content="Created")



@router.get("/users/{id}")
async def get_by_id(id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    else:
        return Response(status_code=200, content="User Found")


@router.patch("/users/{id}")
async def patch_user(id: str, user: PatchUser, db: Session = Depends(get_db)):
    to_patch = db.query(UserModel).filter(UserModel.id == id).first()
    if not to_patch:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    if user.email and db.query(UserModel).filter(UserModel.email == user.email).filter(UserModel.id != id).first():
        raise HTTPException(status_code=409, detail="Email Already Taken")

    to_patch.name = user.name
    to_patch.surname = user.surname
    to_patch.email = user.email
    to_patch.birth_date = user.birth_date
    to_patch.personal_identificator = user.personal_identificator
    to_patch.updated_at = datetime.now()
    db.commit()
    db.refresh(to_patch)
    return to_patch
