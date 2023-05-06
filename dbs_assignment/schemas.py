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

        