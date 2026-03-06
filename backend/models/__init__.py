# Bu dosya, tüm SQLAlchemy modellerini içe aktararak (import), 
# Alembic migrasyonlarında ve Base.metadata.create_all() çağrılarında 
# otomatik olarak kaydedilmelerini sağlar.

from .team import Team
from .player import Player
from .game import Game
from .player_stats import PlayerStat
from .prop_line import PropLine
from .user import User, UserFavorite
from .saved_pick import SavedPick

# Başka yerlerden kolayca import edebilmek için models klasörünün dışa açtığı sınıflar:
__all__ = [
    "Team",
    "Player",
    "Game",
    "PlayerStat",
    "PropLine",
    "User",
    "UserFavorite",
    "SavedPick",
]
