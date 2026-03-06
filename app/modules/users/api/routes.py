from app.modules.users.use_cases.create_users import CreateUser
from app.modules.users.api import schemas
from app.modules.users.infrastructure.sqlalchemy_repository import SQLAlchemyUserRepository
from app.modules.users.use_cases.list_users import ListUsers
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[schemas.UserList])
def read_users(db: Session = Depends(get_db)):
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