import asyncio
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_factory
from services.balldontlie import balldontlie_client
from services.odds_api import odds_client
from services.cache import cache_client
# Modellerimizi ve Analiz motorumuzu import edeceğiz ilerde

logger = logging.getLogger("nba_props_scheduler")

class TaskScheduler:
    """
    Arka planda periyodik olarak veri çeken APScheduler sistemi.
    1. Oranları Güncelleme (Her 5 dk)
    2. İstatistikleri Güncelleme (Her saat)
    3. Tam Senkronizasyon (Günde 2 kere)
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=timezone.utc)

    async def update_odds(self):
        """Her 5 dakikada The Odds API'den güncel bahisleri çeker."""
        logger.info("🏀 [Scheduler] 'update_odds' görev başladı.")
        try:
            # TODO: Veritabanından bugünün yaklaşan maçlarını (event_ids) çek
            # TODO: odds_client ile oranları al ve PropLines tablosuna kaydet
            logger.info("✅ 'update_odds' başarıyla tamamlandı.")
        except Exception as e:
            logger.error(f"❌ 'update_odds' hatası: {e}")

    async def update_player_stats(self):
        """Her saat BallDontLie'den biten maçlardaki oyuncu istatistiklerini günceller."""
        logger.info("🏀 [Scheduler] 'update_player_stats' görev başladı.")
        try:
            # TODO: Bitmiş (Status=Final) ancak istatistiği eksik olan oyunların ID'sini bul
            # TODO: balldontlie_client ile istatistikleri çek, PlayerStats tablosuna kaydet
            logger.info("✅ 'update_player_stats' başarıyla tamamlandı.")
        except Exception as e:
            logger.error(f"❌ 'update_player_stats' hatası: {e}")

    async def full_sync(self):
        """Günde 2 kez tam veri kontrolü (Takımlar, Eksik Oyuncular vs.)."""
        logger.info("🔄 [Scheduler] 'full_sync' görev başladı.")
        try:
            # TODO: Eksik takımlar / yeni transfer oyuncuların listesi vs
            logger.info("✅ 'full_sync' başarıyla tamamlandı.")
        except Exception as e:
            logger.error(f"❌ 'full_sync' hatası: {e}")

    def start(self):
        """Zamanlanmış görevleri başlatır."""
        # 1. Her 5 dakikada oran çekimi
        self.scheduler.add_job(
            self.update_odds, 
            IntervalTrigger(minutes=5), 
            id="update_odds", 
            replace_existing=True
        )
        
        # 2. Her 60 dakikada (saatte bir) istatistikleri çek
        self.scheduler.add_job(
            self.update_player_stats, 
            IntervalTrigger(minutes=60), 
            id="update_player_stats", 
            replace_existing=True
        )

        # 3. Her 12 saatte tam senkronizasyon
        self.scheduler.add_job(
            self.full_sync, 
            IntervalTrigger(hours=12), 
            id="full_sync", 
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("⏱️ Arka plan görev zamanlayıcısı (Scheduler) başlatıldı.")

    def stop(self):
        """Zamanlayıcıyı durdurur."""
        self.scheduler.shutdown()
        logger.info("🛑 Scheduler durduruldu.")

scheduler = TaskScheduler()
