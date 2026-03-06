"""
NBA Props App - FastAPI Ana Modül

Uygulamanın giriş noktası. Tüm router'ları, middleware'leri ve
başlangıç/kapanış olaylarını burada tanımlarız.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Uygulama yaşam döngüsü yöneticisi.
    - Başlangıçta: veritabanı tabloları oluşturulur
                   scheduler başlatılır
    - Kapanışta: veritabanı bağlantısı, redis ve scheduler kapatılır
    """
    from tasks.scheduler import scheduler
    from services.cache import cache_client
    
    print("🏀 NBA Props App başlatılıyor...")
    await init_db()
    print("✅ Veritabanı bağlantısı kuruldu")
    
    # Arkaplan zamanlı veri indirme işlemini başlat (scheduler)
    scheduler.start()
    
    yield
    
    print("🛑 NBA Props App kapatılıyor...")
    scheduler.stop()
    await cache_client.close()
    await close_db()
    print("✅ Bağlantılar başarıyla kapatıldı")


# FastAPI uygulamasını oluştur
app = FastAPI(
    title="NBA Props Analytics API",
    description="NBA oyuncu prop bahis analizleri için REST API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS ayarları — frontend'in backend'e erişmesine izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Next.js dev server
        "http://frontend:3000",      # Docker içi
        "*" if settings.APP_DEBUG else "",  # Debug modda tüm origin'ler
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- API Router'larını ekliyoruz ----
from routers import players, props, picks, users
app.include_router(players.router, prefix="/api/players", tags=["Players"])
app.include_router(props.router, prefix="/api/props", tags=["Props"])
app.include_router(picks.router, prefix="/api/picks", tags=["Picks"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.get("/", tags=["Root"])
async def root():
    """Ana endpoint — API durumunu kontrol eder."""
    return {
        "app": "NBA Props Analytics API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Sağlık kontrolü — servislerin durumunu döndürür."""
    return {
        "status": "healthy",
        "database": "connected",
        "environment": settings.APP_ENV,
    }
