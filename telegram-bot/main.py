import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

# Env dosyasını yükle (Aynı dizindeki veya kök dizindeki)
load_dotenv(dotenv_path="../.env")

# Telegram Bot Token'ı al
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Mini App URL (Kendi domaininize göre değiştireceksiniz. Örn: https://props.benimdomainim.com)
# Telegram sadece HTTPS URL'leri Mini App olarak kabul eder. 
# Geçici test için eğer bilgisayarda deniyorsanız ngrok kullanmalısınız.
MINI_APP_URL = os.getenv("FRONTEND_URL", "https://siteniz-guncellenecek.com")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    if not BOT_TOKEN or "your_token_here" in BOT_TOKEN:
        logger.error("❌ Lütfen .env dosyasında TELEGRAM_BOT_TOKEN tanımlayın.")
        return

    logger.info("🤖 Telegram Bot Başlatılıyor...")
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        """Kullanıcı bota /start dediğinde çalışacak fonksiyon"""
        
        # Mini App açmak için buton
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏀 NBA Statistics App",
                        web_app=WebAppInfo(url=MINI_APP_URL)
                    )
                ]
            ]
        )

        user_name = message.from_user.first_name
        
        welcome_text = (
            f"🏀 Merhaba {user_name}! NBA Player Statistics AI'a hoş geldin.\n\n"
            f"Bu bot üzerinden NBA oyuncularının anlık istatistiklerini görebilir, "
            f"AI tarafından önerilen eşleşme puanı A+ olan maçları bulabilirsin.\n\n"
            f"Tüm analizler için aşağıdaki butona tıklayarak Web Uygulamamızı aç!"
        )

        await message.answer(welcome_text, reply_markup=keyboard)

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        """Kullanıcı /help komutunu girdiğinde"""
        help_text = (
            "🛠️ *NBA Player Statistics - Komut Listesi*\n\n"
            "/start - Ana menüyü ve Mini App butonunu gösterir\n"
            "/top - Bugünün yapay zeka tarafından seçilen en iyi prop önerisi\n"
            "/help - Bu yardım menüsünü gösterir"
        )
        await message.answer(help_text, parse_mode="Markdown")

    @dp.message(Command("top"))
    async def cmd_top(message: types.Message):
        """Basit bir örnek. Gerçek senaryoda Backend API'sine HTTP isteği atılarak güncel prop çekilir."""
        # TODO: C:\Users\mehmet\.gemini\antigravity\nba-props-app\backend\routers\picks.py deki GET /best'i çağır
        test_message = (
            "🔥 *Günün Fırsatı (AI Edge: +5.2%)*\n\n"
            "🏀 *LeBron James* - Points O/U 24.5\n"
            "👉 *Öneri:* OVER (Üst)\n"
            "🛡️ *Matchup Grade:* A+\n"
            "ℹ️ *Not:* Rakip savunma oldukça zayıf."
        )
        await message.answer(test_message, parse_mode="Markdown")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot çalışırken hata oluştu: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
