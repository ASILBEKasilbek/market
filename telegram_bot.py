import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from django.conf import settings
import os
from aiogram import types
from aiogram.types import FSInputFile

# Bot yaratish
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()


async def send_order_notification(order):
    caption = f"""
🛍 Yangi buyurtma!
👕 Mahsulot: {order.product.name}
💰 Narx: {order.product.price} so‘m
📱 Mijoz: {order.user.username}
☎️ Telefon: {order.phone}
📍 Manzil: {order.address}
✍️ Izoh: {order.note}
    """
    if order.product.images.exists():
        try:
            photo_path = order.product.images.first().image.path
            if os.path.exists(photo_path):
                photo = FSInputFile(photo_path)
                await bot.send_photo(
                    chat_id=settings.TELEGRAM_CHAT_ID,
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
                return
        except Exception as e:
            print("Fayl orqali yuborishda xato:", e)
    await bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=caption,
        parse_mode=ParseMode.MARKDOWN
    )

# Polling ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
