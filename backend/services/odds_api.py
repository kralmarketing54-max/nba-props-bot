import httpx
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from config import settings

class OddsAPI:
    """
    The Odds API Client
    Docs: https://the-odds-api.com/liveapi/guides/v4/
    """
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self):
        self.api_key = settings.ODDS_API_KEY
        
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        """The Odds API'ye istek atar ve JSON döner."""
        if params is None:
            params = {}
            
        params["apiKey"] = self.api_key
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=20.0
            )
            response.raise_for_status()
            return response.json()

    # --- SPORTS / BASKETBALL ---
    async def get_active_sports(self) -> List[Dict]:
        """Sistemde aktif olan spor türlerini listeler."""
        return await self._make_request("sports")
        
    async def get_basketball_games(self) -> List[Dict]:
        """
        Yaklaşan NBA maçlarının listesini ('daysFrom' kullanarak) döndürür.
        Sport anahtarı: basketball_nba
        """
        params = {
            "sport": "basketball_nba",
            "regions": "us",
            "markets": "h2h", # Default, sadece maçları listelemek için kullanıyoruz
            "oddsFormat": "american"
        }
        # returns /sports/basketball_nba/odds
        return await self._make_request("sports/basketball_nba/odds", params=params)

    # --- PLAYER PROPS ---
    async def get_player_props(self, event_id: str, market_keys: str = "player_points,player_rebounds,player_assists") -> List[Dict]:
        """
        Belirtilen maç (event_id) içindeki P/R/A vb player prop bahislerini döndürür.
        market_keys alanına birden fazla market virgülle yazılarak girilebilir.
        Örn: 'player_points,player_rebounds,player_assists,player_threes'
        """
        params = {
            "regions": "us",              # bookmaker olarak us sirketleri DraftKings, FanDuel vs.
            "markets": market_keys,
            "oddsFormat": "american",
            "bookmakers": "draftkings,fanduel,betmgm" # Spesifik güvenilir bookmaker listesi (Optimizasyon için)
        }
        # Endpoint formati: /sports/basketball_nba/events/{eventId}/odds
        return await self._make_request(f"sports/basketball_nba/events/{event_id}/odds", params=params)

# Ortak kullanım için instance
odds_client = OddsAPI()
