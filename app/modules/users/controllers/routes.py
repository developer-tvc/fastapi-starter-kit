from app.modules.users.services.create_users import CreateUser
from app.modules.users.controllers import schemas
from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository
from app.modules.users.services.list_users import ListUsers
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.modules.users.entities.entities import User
from app.core.dependencies import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[schemas.UserList])
def read_users(db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    repo = SQLAlchemyUserRepository(db)
    use_case = ListUsers(repo)
    return use_case.execute()


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,  # Request body containing user data
    db: Session = Depends(get_db),  # Inject database session
):
    repo = SQLAlchemyUserRepository(db)
    use_case = CreateUser(repo)
    return use_case.execute(user.email, user.password, user.full_name)