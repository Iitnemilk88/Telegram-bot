from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Константы
BOT_TOKEN = "7601748735:AAEe3aIX8OSBH4-W-0vz3_IB_SEhg30TmRI"  # Замените на токен вашего бота

# Функция для получения ID чата
async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"ID вашей группы: {chat_id}")

# Основная функция для запуска бота
def main() -> None:
    # Создаем приложение Telegram
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчик команды /get_id
    application.add_handler(CommandHandler("get_id", get_group_id))

    # Запускаем приложение
    application.run_polling()

if __name__ == "__main__":
    main()
