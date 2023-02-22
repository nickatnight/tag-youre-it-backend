from src.models.player import Player
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.player import IPlayerCreate, IPlayerUpdate


class PlayerRepository(BaseSQLAlchemyRepository[Player, IPlayerCreate, IPlayerUpdate]):
    _model = Player
