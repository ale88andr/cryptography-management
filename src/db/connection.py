from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class AsyncDatabaseSession:
    def __init__(self, connection_url: str):
        self.session = None
        self.engine = None
        self.connection_url = connection_url

    def __getattr__(self, attr):
        return getattr(self.session, attr)

    def init(self):
        self.engine = create_async_engine(
            self.connection_url,
            echo=True,
            connect_args={"server_settings": {"jit": "off"}},
            isolation_level="AUTOCOMMIT",
        )
        self.session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )()


db = AsyncDatabaseSession(settings.db_connection_string)


class Base(DeclarativeBase):

    def __repr__(self) -> str:
        # props = [f"{c}={getattr(self, c)}" for c in self.__table__.columns.keys()]
        # return f"<{self.__class__.__name__}: {', '.join(props)}>"
        return f"<{self.__class__.__name__}: {self.id}>"
