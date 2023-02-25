from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.base import BaseModel
from src.models.link import GamePlayerLink


if TYPE_CHECKING:
    from src.models.player import Player
    from src.models.subreddit import SubReddit


class GameBase(SQLModel):
    subreddit_id: int = Field(
        default=None, foreign_key="subreddit.id", description="The database id of the subreddit"
    )
    is_active: Optional[bool] = Field(default=True, description="Is the Game active or not.")


class Game(BaseModel, GameBase, table=True):
    subreddit: Optional["SubReddit"] = Relationship(
        back_populates="games", sa_relationship_kwargs={"lazy": "selectin"}
    )
    players: List["Player"] = Relationship(
        back_populates="games",
        link_model=GamePlayerLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
