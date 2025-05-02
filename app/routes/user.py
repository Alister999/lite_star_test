from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, post, get, put, delete
from litestar.exceptions import HTTPException

from app.dto.user_dto import UserDTO
# from app.main import app
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.user_repo import UserRepository


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserDTO, db_session: AsyncSession) -> UserDTO:
        user_data = data.dict(exclude={"created_at", "updated_at"})

        new_user = User(**user_data.dict())
        repo = UserRepository(session=db_session)
        await repo.add(new_user)#list()
        await db_session.refresh(new_user)
        return new_user

        # user = User(**data.dict())
        # db_session.add(user)
        # await db_session.commit()
        # return user

    @get()
    async def list_users(self, db_session: AsyncSession, limit: int = 100, offset: int = 0) -> list[UserDTO]:
        repo = UserRepository(session=db_session)
        users = await repo.list(limit=limit, offset=offset)
        return users

        # result = await db_session.execute(select(User))
        # users = result.scalars().all()
        # return users


    @get("/{user_id:int}")
    async def get_user(self, user_id: int, db_session: AsyncSession) -> UserDTO:
        repo = UserRepository(session=db_session)
        # user = await repo.get(user_id)#list()
        try:
            return await repo.get(user_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")



        # if not user:
        #     raise HTTPException(status_code=404, detail='Missing user by this id.')
        # return user

        # result = await db_session.get(User, user_id)
        # return result


    @put("/{user_id:int}")
    async def update_user(self, user_id: int, data: UserDTO, db_session: AsyncSession) -> UserDTO:
        repo = UserRepository(session=db_session)
        try:
            change_user = await repo.get(user_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        user_data = data.dict(exclude={"created_at", "updated_at"})
        for key, value in user_data.items():
            setattr(change_user, key, value)

        updated_user = await repo.update(change_user)
        return updated_user



        # change_user = await repo.get(user_id)
        # if not change_user:
        #     raise HTTPException(status_code=404, detail='Missing user by this id.')
        # for key, value in data.dict().items():
        #     setattr(change_user, key, value)
        #
        # return change_user

        # user = await db_session.get(User, user_id)
        # for key, value in data.dict().items():
        #     setattr(user, key, value)
        # await db_session.commit()
        # return user

    @delete("/{user_id:int}", status_code=200)
    async def delete_user(self, user_id: int, db_session: AsyncSession) -> None:
        repo = UserRepository(session=db_session)
        try:
            delete_user = await repo.get(user_id)
            await repo.delete(delete_user)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")




        # delete_user = await repo.get(user_id)
        # if not delete_user:
        #     raise HTTPException(status_code=404, detail='Missing user by this id.')
        # await repo.delete(delete_user)
        #
        # return {"deleted": True}

        # user = await db_session.get(User, user_id)
        # await db_session.delete(user)
        # await db_session.commit()
        # return {"deleted": True}

user_routes = UserController
