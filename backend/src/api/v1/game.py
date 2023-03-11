from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import OrderEnum, SortEnum
from src.db.session import get_session
from src.repositories.game import GameRepository
from src.schemas.common import IGetResponseBase
from src.schemas.game import IGameRead


router = APIRouter()


@router.get(
    "/games",
    response_description="List all Game instances",
    response_model=IGetResponseBase[List[IGameRead]],
    tags=["games"],
)
async def games(
    response: Response,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    sort: str = Query(default=SortEnum.CREATED_AT),
    order: str = Query(default=OrderEnum.DESC),
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[IGameRead]]:
    repo = GameRepository(db=session)
    games = await repo.all(skip=skip, limit=limit, sort_field=sort, sort_order=order.lower())

    response.headers["x-content-range"] = f"{len(games)}/{limit}"
    return IGetResponseBase[List[IGameRead]](data=games)
