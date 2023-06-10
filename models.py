from __future__ import annotations

from typing import List
from typing_extensions import Self

import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs
)
from sqlalchemy.orm import (
    mapped_column,
    DeclarativeBase,
    Mapped
)
from sqlalchemy.sql import func

from config import config


class Base(AsyncAttrs, DeclarativeBase):
    @classmethod
    async def add(
        cls,
        **kw
    ) -> None:
        async with async_session() as session:
            async with session.begin():
                session.add(cls(**kw))

    @classmethod
    async def find(
        cls,
        *whereclause
    ) -> List[Self]:
        async with async_session() as session:
            async with session.begin():
                statement = sqla.select(cls)
                if len(whereclause) != 0:
                    statement = statement.where(*whereclause)

                result = await session.execute(statement)
                return [model for (model, ) in result.all()]

    @classmethod
    async def delete(
        cls,
        *whereclause
    ) -> None:
        async with async_session() as session:
            async with session.begin():
                statement = sqla.delete(cls)
                if len(whereclause) != 0:
                    statement = statement.where(*whereclause)

                await session.execute(statement)


class Subscription(Base):
    __tablename__ = "subscribed_guild"

    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(sqla.BigInteger)
    channel_id: Mapped[int] = mapped_column(sqla.BigInteger)
    game_id: Mapped[str]


class Game(Base):
    __tablename__ = "modio_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[str]


class SendedEvent(Base):
    __tablename__ = "sended_mod_event"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(sqla.BigInteger)
    mod_file_id: Mapped[int] = mapped_column(sqla.BigInteger)
    game_id: Mapped[str]
    data_added = mapped_column(sqla.DateTime(), server_default=func.now())


async def setup() -> None:
    global async_session

    engine = create_async_engine(config.db_uri)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
