from db.config import async_session
from db.dals.users_dal import UserDAL


async def get_user_dal() -> UserDAL:
    async with async_session() as session:
        async with session.begin():
            return UserDAL(session)
