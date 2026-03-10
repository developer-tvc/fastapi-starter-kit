from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.auth.services.user_login import LoginUserService
from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository
from app.modules.auth.controllers import schemas

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/login")
async def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    use_case = LoginUserService(repo)
    return await use_case.execute(request.email, request.password)