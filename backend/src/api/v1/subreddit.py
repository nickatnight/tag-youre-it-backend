from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.repositories.subreddit import SubRedditRepository
from src.schemas.common import IGetResponseBase
from src.schemas.subreddit import ISubRedditRead


router = APIRouter()


@router.get(
    "/subreddits",
    response_description="List all SubReddit instances",
    response_model=IGetResponseBase[List[ISubRedditRead]],
    tags=["subreddits"],
)
async def subreddits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[ISubRedditRead]]:
    repo = SubRedditRepository(db=session)
    subreddits = await repo.all(skip=skip, limit=limit)

    return IGetResponseBase[List[ISubRedditRead]](data=subreddits)
