from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[IGameRead]:
    repo = GameRepository(db=session)
    games = await repo.all(skip=skip, limit=limit)

    return IGetResponseBase[List[IGameRead]](data=games)
