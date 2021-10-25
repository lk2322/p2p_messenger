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
        await self.db_session.flush()

    async def get_users(self, usr_id: int) -> List[Users]:
        # TODO доделать
        q = await self.db_session.query()
        return q.scalars().first()
