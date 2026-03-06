import httpx
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from config import settings

class BallDontLieAPI:
    """
    BallDontLie API Client (v1)
    Docs: https://docs.balldontlie.io/
    """
    
    BASE_URL = "https://api.balldontlie.io/v1"
    
    def __init__(self):
        # Header'lara API key ekliyoruz
        self.headers = {
            "Authorization": f"{settings.BALLDONTLIE_API_KEY}"
        }
        
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """API'ye istek atar ve JSON döner. Hata durumunda exception fırlatır."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/{endpoint}",
                headers=self.headers,
                params=params,
                timeout=15.0
            )
            response.raise_for_status()
            return response.json()

    # --- TEAMS ---
    async def get_all_teams(self) -> List[Dict]:
        """Tüm NBA takımlarını getirir (30 takım)."""
        response = await self._make_request("teams")
        return response.get("data", [])

    # --- PLAYERS ---
    async def search_players(self, search_query: str) -> List[Dict]:
        """İsme veya soyisme göre oyuncu arar."""
        response = await self._make_request("players", params={"search": search_query})
        return response.get("data", [])
        
    async def get_active_players(self, cursor: int = None) -> Dict:
        """Gelen cursor'a göre aktif oyuncuları sayfalı getirir."""
        # Yalnızca aktif oyuncuları almak için API desteklemiyorsa 
        # son yıllara göre veritabanında filtreleyeceğiz
        params = {"per_page": 100}
        if cursor:
            params["cursor"] = cursor
            
        return await self._make_request("players", params=params)

    # --- GAMES ---
    async def get_games_by_date(self, dates: List[str]) -> List[Dict]:
        """
        Belirtilen tarihlerdeki maçları getirir. 
        Format: YYYY-MM-DD
        """
        # API'nin beklediği format argüman isimleri: dates[]=2024-01-01
        params = [("dates[]", d) for d in dates]
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/games",
                headers=self.headers,
                params=params,
                timeout=15.0
            )
            response.raise_for_status()
            return response.json().get("data", [])

    # --- STATS ---
    async def get_player_stats(self, player_ids: List[int], seasons: List[int], per_page: int = 100) -> List[Dict]:
        """
        Belirli oyuncuların belirtilen sezondaki maç istatistiklerini getirir.
        """
        params = [("per_page", per_page)]
        for pid in player_ids:
            params.append(("player_ids[]", pid))
        for season in seasons:
            params.append(("seasons[]", season))
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/stats",
                headers=self.headers,
                params=params,
                timeout=20.0
            )
            response.raise_for_status()
            return response.json().get("data", [])

# Tüm servislerde ortak kullanım için bir instance oluşturuyoruz
balldontlie_client = BallDontLieAPI()
