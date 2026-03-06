from typing import List, Dict, Any
from models.player_stats import PlayerStat
from models.game import Game

class AnalyticsService:
    """
    Oyuncu istatistikleri üzerinden matematiksel analizler yapar.
    Props hit rate, Home/Away split, Head-to-Head (H2H) hesaplamalarını yönetir.
    """

    @staticmethod
    def _get_stat_value_for_market(stat: PlayerStat, market: str) -> float:
        """
        Belirtilen markete (points, rebounds, vs.) göre oyuncunun maçtaki istatistiğini döndürür.
        """
        if market == "player_points":
            return float(stat.pts or 0)
        elif market == "player_rebounds":
            return float(stat.reb or 0)
        elif market == "player_assists":
            return float(stat.ast or 0)
        elif market == "player_threes":
            return float(stat.fg3m or 0)
        elif market == "player_points_rebounds_assists":
            return float((stat.pts or 0) + (stat.reb or 0) + (stat.ast or 0))
        elif market == "player_points_rebounds":
            return float((stat.pts or 0) + (stat.reb or 0))
        elif market == "player_points_assists":
            return float((stat.pts or 0) + (stat.ast or 0))
        elif market == "player_rebounds_assists":
            return float((stat.reb or 0) + (stat.ast or 0))
        elif market == "player_steals":
            return float(stat.stl or 0)
        elif market == "player_blocks":
            return float(stat.blk or 0)
        elif market == "player_blocks_steals":
            return float((stat.blk or 0) + (stat.stl or 0))
        elif market == "player_turnovers":
            return float(stat.turnover or 0)
        return 0.0

    @classmethod
    def calculate_hit_rate(cls, stats: List[PlayerStat], market: str, line: float, games_count: int = None) -> Dict[str, Any]:
        """
        Verilen maç listesi ve line değeri için Hit Rate (Over vurma oranı) hesaplar.
        """
        if not stats:
            return {"hit_rate": 0, "hits": 0, "total": 0, "history": []}

        # Maç sayısına göre filtrele (örn: Son 5 maç)
        target_stats = stats[:games_count] if games_count else stats
        total_games = len(target_stats)
        
        if total_games == 0:
            return {"hit_rate": 0, "hits": 0, "total": 0, "history": []}

        hits = 0
        history = []
        
        for stat in target_stats:
            value = cls._get_stat_value_for_market(stat, market)
            is_hit = value > line # Push (tie) over sayılmaz.
            if is_hit:
                hits += 1
                
            history.append({
                "game_id": stat.game_id,
                "value": value,
                "line": line,
                "is_hit": is_hit
            })

        hit_rate = (hits / total_games) * 100

        return {
            "hit_rate": round(hit_rate, 2),
            "hits": hits,
            "total": total_games,
            "history": history
        }

    @classmethod
    def get_comprehensive_hit_rates(cls, stats: List[PlayerStat], market: str, line: float) -> Dict[str, Any]:
        """Son 5, Son 10, Son 20 ve Sezon Ortalaması hit oranlarını toplu halde verir."""
        # Stats listesinin tarihe göre azalan (en yeniden en eskiye) sıralı olması beklenir
        return {
            "l5": cls.calculate_hit_rate(stats, market, line, 5),
            "l10": cls.calculate_hit_rate(stats, market, line, 10),
            "l20": cls.calculate_hit_rate(stats, market, line, 20),
            "season": cls.calculate_hit_rate(stats, market, line, None) # Tüm maçlar
        }

    @classmethod
    def calculate_splits(cls, stats: List[PlayerStat], current_team_id: int, opponent_team_id: int, market: str) -> Dict[str, float]:
        """
        Home/Away ve Head-to-Head istatistik ortalamalarını hesaplar.
        Parametreler için 'Game' objesinin eager load (joinedload) edilmiş olması gerekir.
        """
        home_games = []
        away_games = []
        h2h_games = []
        
        for stat in stats:
            if not stat.game:
                continue
                
            value = cls._get_stat_value_for_market(stat, market)
            
            # Home/Away
            is_home = (stat.game.home_team_id == current_team_id)
            if is_home:
                home_games.append(value)
            else:
                away_games.append(value)
                
            # Head-to-Head
            if stat.game.home_team_id == opponent_team_id or stat.game.away_team_id == opponent_team_id:
                h2h_games.append(value)

        return {
            "home_avg": round(sum(home_games) / len(home_games), 2) if home_games else 0.0,
            "away_avg": round(sum(away_games) / len(away_games), 2) if away_games else 0.0,
            "h2h_avg": round(sum(h2h_games) / len(h2h_games), 2) if h2h_games else 0.0,
            "h2h_games_count": len(h2h_games)
        }

analytics_service = AnalyticsService()
