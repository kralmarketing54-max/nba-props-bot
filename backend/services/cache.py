import redis.asyncio as redis
import json
from typing import Any, Optional
from config import settings

class CacheService:
    """
    Redis Cache Service.
    Sık sorulan verileri API/DB yükünü azaltmak için önbellekte tutar.
    """

    def __init__(self):
        # Async redis connection pool'u başlatır.
        self.redis = redis.from_url(
            settings.REDIS_URL, 
            encoding="utf-8", 
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        """Belirtilen anahtara ait veriyi getirir."""
        data = await self.redis.get(key)
        if data:
            try:
                # JSON deserialize
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        return None

    async def set(self, key: str, value: Any, expire_seconds: int = 3600):
        """Veriyi Redis'te expire time (saniye) ile saklar."""
        # Eğer python dict veya list ise JSON a çevir
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
            
        await self.redis.set(name=key, value=value, ex=expire_seconds)

    async def delete(self, key: str):
        """Belirtilen anahtarı siler."""
        await self.redis.delete(key)

    async def flush(self):
        """Tüm cache'i temizler (Dikkatli kullanılmalı)."""
        await self.redis.flushdb()
        
    async def close(self):
        """Bağlantıyı kapatır."""
        await self.redis.close()

# Servislerde ortak kullanım için instance
cache_client = CacheService()
