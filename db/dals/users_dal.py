from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.users import Users


class UserDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, name: str, ip: str, hashed_private_key: bytes, hashed_public_key: bytes,
                          hashed_public_key_addr: bytes):
        new_user = Users(name=name, ip=ip, hashed_private_key=hashed_private_key, hashed_public_key=hashed_public_key,
                         hashed_public_key_addr=hashed_public_key_addr)
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.close()


    async def get_all_users(self) -> List[Users]:
        q = await self.db_session.execute(select(Users).order_by(Users.id))
        await self.db_session.close()
        return q.scalars().all()