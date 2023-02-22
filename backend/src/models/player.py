from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from src.models.base import BaseModel
from src.models.link import GamePlayerLink


class PlayerBase(SQLModel):
    """aPRAW fields

    NOTE: Suspended Redditors only return is_suspended and name.
    """

    reddit_id: str = Field(..., description="The ID of the Redditor.")
    username: str = Field(sa_column_kwargs={"unique": True}, description="The Redditor’s username.")
    icon_img: str = Field(..., description="The url of the Redditors’ avatar.")
    is_employee: bool = Field(..., description="Whether or not the Redditor is a Reddit employee.")
    verified: bool = Field(..., description="Whether the Redditor is verified.")
    has_verified_email: bool = Field(
        ..., description="Whether the Redditor has a verified email address."
    )
    created_utc: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
        description="Time the account was created, represented in Unix Time.",
    )
    is_suspended: Optional[bool] = Field(
        default=False, description="Whether the Redditor has been suspended."
    )
    # game fields
    opted_out: Optional[bool] = Field(default=False, description="Did the user opt out of playing.")
    is_banned: Optional[bool] = Field(default=False, description="Is the user banned from playing.")
    tag_time: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
        description="What time did the user get tagged. Sets to None once they tag another user.",
    )


class Player(BaseModel, PlayerBase, table=True):
    games: List["Game"] = Relationship(back_populates="players", link_model=GamePlayerLink, sa_relationship_kwargs={"lazy": "selectin"})  # type: ignore # noqa
