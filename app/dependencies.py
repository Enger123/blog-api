from typing import Annotated
from auth.jwt import get_current_user
from fastapi.params import Depends
from schemas.post import PaginationParams
from models import User
from app.database import Session

CurrentUser = Annotated[User, Depends(get_current_user)]
PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[Session, Depends(get_db)]
