from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings


test_engine = create_async_engine(
    settings.POSTGRES_URL, echo=False, future=True, pool_size=settings.POOL_SIZE, max_overflow=64
)
