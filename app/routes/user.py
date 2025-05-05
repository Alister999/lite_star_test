from contextlib import asynccontextmanager
from datetime import datetime, timezone
from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, post, get, put, delete
from litestar.di import Provide
from litestar.exceptions import HTTPException
from sqlalchemy import update

from app.config import db_config
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.pydantic.user_pd import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repo import UserRepository


@asynccontextmanager
async def no_autoflush(session: AsyncSession):
    autoflush = session.autoflush
    session.autoflush = False
    try:
        yield
    finally:
        session.autoflush = autoflush


async def get_db() -> AsyncSession:
    async with db_config.get_session() as session:
        yield session


class UserController(Controller):
    path = "/users"
    dependencies = {"db_session": Provide(get_db)}

    @post()
    async def create_user(self, data: UserCreate, db_session: AsyncSession) -> UserCreate:
        user_data = data.dict(exclude_unset=True, exclude={"created_at", "updated_at"})

        new_user = User(**user_data)#.dict())
        repo = UserRepository(session=db_session)
        await repo.add(new_user)#list()
        await db_session.commit()
        await db_session.refresh(new_user)
        return UserCreate.from_orm(new_user)


    @get()
    async def list_users(self, db_session: AsyncSession) -> list[UserResponse]:
        repo = UserRepository(session=db_session)
        users = await repo.list()
        return [UserResponse.from_orm(user) for user in users]


    @get("/{user_id:int}")
    async def get_user(self, user_id: int, db_session: AsyncSession) -> UserResponse:
        repo = UserRepository(session=db_session)
        try:
            get_user = await repo.get(user_id)
            return UserResponse.from_orm(get_user)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")


    @put("/{user_id:int}")
    async def update_user(self, user_id: int, data: UserUpdate, db_session: AsyncSession) -> UserResponse:
        user_data = data.dict(exclude_unset=True)
        user_data["updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
        async with no_autoflush(db_session):
            result = await db_session.execute(
                update(User).where(User.id == user_id).values(**user_data)
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
            await db_session.commit()
            updated_user = await db_session.get(User, user_id)
            return UserResponse.from_orm(updated_user)


    @delete("/{user_id:int}", status_code=200)
    async def delete_user(self, user_id: int, db_session: AsyncSession) -> None:
        repo = UserRepository(session=db_session)
        try:
            await repo.delete(user_id)
            await db_session.commit()
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")


user_routes = UserController
