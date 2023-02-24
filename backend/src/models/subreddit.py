from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.base import BaseModel


if TYPE_CHECKING:
    from src.models.game import Game


class SubRedditBase(SQLModel):
    # aPRAW fields
    name: str = Field(description="The database name of the subreddit")
    sub_id: str = Field(description="The Reddit Id of the subreddit")
    display_name: str = Field(description="The human friendly name of the subreddit")
    created_utc: int = Field(
        description="Time the subreddit was created, represented in Unix Time."
    )
    description: str = Field(description="Subreddit description, in Markdown.")
    description_html: str = Field(description="Subreddit description, in HTML.")
    over18: bool = Field(description="Whether the subreddit is NSFW.")
    subscribers: int = Field(description="Count of subscribers.")
    icon_img: str = Field(description="The url of the Subreddit icon img.")
    # custom
    is_banned: Optional[bool] = Field(
        default=False, description="Is the bot banned from the Subreddit."
    )


class SubReddit(BaseModel, SubRedditBase, table=True):
    games: Optional[List["Game"]] = Relationship(
        back_populates="subreddit", sa_relationship_kwargs={"lazy": "selectin"}
    )
