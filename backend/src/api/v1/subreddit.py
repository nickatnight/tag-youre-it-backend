from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import OrderEnum, SortEnum
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
    response: Response,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    sort: str = Query(default=SortEnum.CREATED_AT),
    order: str = Query(default=OrderEnum.DESC),
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[ISubRedditRead]]:
    repo = SubRedditRepository(db=session)
    subreddits = await repo.all(skip=skip, limit=limit, sort_field=sort, sort_order=order.lower())

    response.headers["x-content-range"] = f"{len(subreddits)}/{limit}"
    return IGetResponseBase[List[ISubRedditRead]](data=subreddits)
