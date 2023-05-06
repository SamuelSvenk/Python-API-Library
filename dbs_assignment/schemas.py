from pydantic import BaseModel
from sqlalchemy.dialects import postgresql

class User(BaseModel):
    id: str
    name: str   
    surname: str   
    email: str
    birth_date: str 
    personal_identificator: str
    created_at: str = None
    updated_at: str = None
    is_childuser: bool = False

class PatchUser(BaseModel):
    name: str = None
    surname: str = None
    email: str = None
    birth_date: str = None
    personal_identificator: str = None
    updated_at: str = None
    is_childuser: bool = None

class CardStatus(str, postgresql.ENUM):
    active = "active"
    inactive = "inactive"
    expired = "expired"

class Card(BaseModel):
    id: str = None
    user_id: str
    magstripe: str   
    status: CardStatus
    created_at: str = None
    updated_at: str = None

class PatchCard(BaseModel):
    status: CardStatus = None
    magstripe: str = None
    created_at: str = None
    updated_at: str = None

class Author(BaseModel):
    id: str
    name: str
    surname: str
    created_at: str = None
    updated_at: str = None

class PatchAuthor(BaseModel):
    name: str = None
    surname: str = None
    created_at: str = None
    updated_at: str = None

class Category(BaseModel):
    id: str
    name: str
    created_at: str = None
    updated_at: str = None

class PatchCategory(BaseModel):
    name: str = None
    created_at: str = None
    updated_at: str = None

class Publication(BaseModel):
    id: str
    title: str
    authors: list
    categories: list
    created_at: str = None
    updated_at: str = None

class Instance(BaseModel):
    id: str
    type: str
    publisher: str
    year : str
    status: str
    publication_id: str
    created_at: str = None
    updated_at: str = None

class Rental(BaseModel):
    id: str
    user_id: str
    publication_id: str
    duration: str
    start_date: str = None
    end_date: str = None

class Reservation(BaseModel):
    id: str
    user_id: str
    publication_id: str
    created_at: str = None

