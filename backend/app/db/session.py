from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create Async Engine for PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Create an Async Session
async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False  # type: ignore[arg-type]
)


# Dependency for routes to use DB session
async def get_db():
    async with async_session_maker() as session:  # type: ignore[arg-type]
        yield session
