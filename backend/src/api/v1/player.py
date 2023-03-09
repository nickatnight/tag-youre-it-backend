from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import OrderEnum, SortEnum
from src.db.session import get_session
from src.repositories.player import PlayerRepository
from src.schemas.common import IGetResponseBase
from src.schemas.player import IPlayerRead


router = APIRouter()


@router.get(
    "/players",
    response_description="List all Player instances",
    response_model=IGetResponseBase[List[IPlayerRead]],
    tags=["players"],
)
async def players(
    response: Response,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    sort: str = Query(default=SortEnum.CREATED_AT),
    order: str = Query(default=OrderEnum.DESC),
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[IPlayerRead]]:
    repo = PlayerRepository(db=session)
    players = await repo.all(skip=skip, limit=limit, sort_field=sort, sort_order=order.lower())

    response.headers["x-content-range"] = f"{len(players)}/{10}"
    return IGetResponseBase[List[IPlayerRead]](data=players)
