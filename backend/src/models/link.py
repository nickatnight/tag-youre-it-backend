from typing import Optional

from sqlmodel import Field, SQLModel


class GamePlayerLink(SQLModel, table=True):
    game_id: Optional[int] = Field(default=None, foreign_key="game.id", primary_key=True)
    player_id: Optional[int] = Field(default=None, foreign_key="player.id", primary_key=True)
