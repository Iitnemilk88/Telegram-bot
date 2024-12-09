import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список поз, вынесенный в константу
POSES = [
    "Объятия на диване",
    "Поза ложки",
    "Классическая миссионерская",
    "Наездница",
    "Поза 69",
    "Догги-стайл",
    "Обратная наездница",
    "Поза лотоса",
    "Сидя на стуле",
    "На столе",
]

async def start_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /start.
    Приветствует пользователя и сообщает о доступных командах.
    """
    try:
        await update.message.reply_text(
            "Привет! Я бот, который поможет вам разнообразить ваши вечера. "
            "Попробуйте команду /random, чтобы получить случайную позу."
        )
    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")

async def random_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /random.
    Отправляет случайную позу из списка.
    """
    try:
        random_pose = random.choice(POSES)
        await update.message.reply_text(f'Попробуйте эту позу: {random_pose}')
    except Exception as e:
        logger.error(f"Ошибка в обработчике /random: {e}")

def main() -> None:
    """
    Основная функция, запускающая бота.
    """
    try:
        # Замените строку ниже вашим токеном
        BOT_TOKEN = "7601748735:AAEe3aIX8OSBH4-W-0vz3_IB_SEhg30TmRI"

        # Создание приложения
        application = Application.builder().token(BOT_TOKEN).build()

        # Регистрация обработчиков команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("random", random_command))

        # Запуск бота
        logger.info("Бот запущен.")
        application.run_polling()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
