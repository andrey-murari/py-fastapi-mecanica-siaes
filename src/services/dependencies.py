from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.repository.database import database

SessionDep = Annotated[Session, Depends(database.get_session)]
