from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from models import Base


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    async def get_session_dependency(self):
        async with self.async_session() as session:
            yield session

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(url=settings.DATABASE_URL)
