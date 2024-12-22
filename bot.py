import asyncio
import logging
import os
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.ext import ApplicationBuilder
from bs4 import BeautifulSoup

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not BOT_TOKEN or not GROUP_ID:
    logger.critical("Отсутствуют необходимые переменные окружения: BOT_TOKEN или GROUP_ID")
    exit(1)

# Инициализация бота
application = ApplicationBuilder().token(BOT_TOKEN).build()
bot = Bot(BOT_TOKEN)

# Функция для парсинга RSS-ленты anekdot.ru
def parse_anekdot_ru():
    url = "https://www.anekdot.ru/rss/export_j.xml"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "xml")

        # Извлекаем заголовки и тексты анекдотов
        jokes = []
        for item in soup.find_all("item"):
            title = item.find("title").text
            description = item.find("description").text
            jokes.append(f"*{title}*\n\n{description}")

        return jokes
    except Exception as e:
        logger.error(f"Ошибка при парсинге anekdot.ru: {e}")
        return []

# Функция отправки анекдотов
async def send_jokes():
    logger.info("Парсим источники с анекдотами")

    jokes_anekdot = parse_anekdot_ru()

    if not jokes_anekdot:
        message = "*Анекдоты*\n\n(Нет новых анекдотов)"
    else:
        message = "*Анекдоты*\n\n" + "\n\n".join(jokes_anekdot[:5])  # Ограничение на 5 анекдотов

    try:
        await bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="Markdown")
        logger.info("Анекдоты успешно отправлены.")
    except Exception as e:
        logger.error(f"Ошибка при отправке анекдотов: {e}")

# Главная функция
def main():
    # Создаем новый цикл событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Планировщик задач
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(send_jokes, "interval", hours=24)  # Запуск каждые 24 часа
    scheduler.start()

    logger.info("Бот запущен и планировщик задач активирован.")

    # Запуск цикла событий
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
