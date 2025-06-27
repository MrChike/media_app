from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.connection import SessionLocal


# PostgreSQL: Dependency to get DB session
async def movies_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
