from litestar import Controller, post, get, put, delete
from app.dto.user_dto import UserDTO
# from app.main import app
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserDTO, db_session: AsyncSession) -> User:
        user = User(**data.dict())
        db_session.add(user)
        await db_session.commit()
        return user

    @get()
    async def list_users(self, db_session: AsyncSession) -> list[User]:
        result = await db_session.execute(select(User))
        return result.scalars().all()

    @get("/{user_id:int}")
    async def get_user(self, user_id: int, db_session: AsyncSession) -> User:
        result = await db_session.get(User, user_id)
        return result

    @put("/{user_id:int}")
    async def update_user(self, user_id: int, data: UserDTO, db_session: AsyncSession) -> User:
        user = await db_session.get(User, user_id)
        for key, value in data.dict().items():
            setattr(user, key, value)
        await db_session.commit()
        return user

    @delete("/{user_id:int}", status_code=200)
    async def delete_user(self, user_id: int, db_session: AsyncSession) -> dict:
        user = await db_session.get(User, user_id)
        await db_session.delete(user)
        await db_session.commit()
        return {"deleted": True}

user_routes = UserController
