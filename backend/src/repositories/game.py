from src.models.game import Game
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.game import IGameCreate, IGameUpdate


class GameRepository(BaseSQLAlchemyRepository[Game, IGameCreate, IGameUpdate]):
    _model = Game
