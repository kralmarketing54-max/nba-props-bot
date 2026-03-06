"""
NBA Props App - Veritabanı Bağlantı Modülü

SQLAlchemy async engine ve session yönetimi.
Her istek için ayrı bir session oluşturur ve işlem sonunda kapatır.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Async veritabanı motoru oluştur
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_DEBUG,  # Debug modda SQL sorgularını logla
    pool_size=20,             # Bağlantı havuzu boyutu
    max_overflow=10,          # Havuz dolunca ek bağlantı sayısı
)

# Session factory — her istek için yeni session üretir
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Tüm SQLAlchemy modellerinin temel sınıfı."""
    pass


async def get_db() -> AsyncSession:
    """
    FastAPI dependency injection için veritabanı session'ı döndürür.

    Kullanım:
        @router.get("/example")
        async def example(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Veritabanı tablolarını oluşturur (geliştirme ortamı için)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Veritabanı bağlantısını kapatır."""
    await engine.dispose()
