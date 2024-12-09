import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список поз, вынесенный в константу
POSES = [
    ("Объятия на диване", "Партнеры сидят на диване, обнимают друг друга, расслаблены и наслаждаются близостью."),
    ("Поза ложки", "Партнеры лежат на боку, один за другим, обвив друг друга руками."),
    ("Классическая миссионерская", "Один партнер лежит на спине, второй сверху, лицом к первому."),
    ("Наездница", "Один партнер лежит на спине, второй сидит сверху, лицом к партнеру."),
    ("Поза 69", "Оба партнера лежат головой вниз и выполняют оральные ласки друг другу."),
    ("Догги-стайл", "Один партнер стоит на коленях и ладонях, а второй партнер находится на коленях сзади."),
    ("Обратная наездница", "Один партнер лежит на спине, второй сидит сверху, спиной к партнеру."),
    ("Поза лотоса", "Один партнер сидит с перекрещенными ногами, другой садится ему на колени, лицом к партнеру."),
    ("Сидя на стуле", "Один партнер сидит на стуле, другой сидит ему на коленях лицом к нему."),
    ("На столе", "Один партнер сидит на столе, второй стоит перед ним или между его ног."),
]

# Настройки обработки команд
async def start_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /start.
    Приветствует пользователя и показывает кнопки для выбора позы.
    """
    try:
        if update.message:  # Если сообщение пришло через команду
            chat = update.message.chat
        elif update.callback_query:  # Если сообщение через кнопку
            chat = update.callback_query.message.chat
        else:
            return  # Ничего не делаем, если нет ни message, ни callback_query

        keyboard = [
            [InlineKeyboardButton("💚 Получить случайную позу 💚", callback_data='random_pose')],
            [InlineKeyboardButton("⛔ Остановить ⛔", callback_data='stop')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await chat.send_message(
            "Привет! Я бот, который поможет вам разнообразить ваши вечера. "
            "Нажмите кнопку ниже, чтобы получить случайную позу.",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")

async def random_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик для случайной позы.
    Отправляет случайную позу с описанием.
    """
    try:
        random_pose, description = random.choice(POSES)
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(
            f'Попробуйте эту позу: {random_pose}\nОписание: {description}'
        )
        # После ответа на кнопки снова предлагается выбор
        keyboard = [
            [InlineKeyboardButton("💚 Получить другую позу 💚", callback_data='random_pose')],
            [InlineKeyboardButton("⛔ Остановить ⛔", callback_data='stop')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(
            "Хотите попробовать еще одну? Нажмите кнопку ниже.",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка в обработчике random_command: {e}")

async def stop_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды 'stop', заменяет сообщение кнопкой для старта.
    """
    try:
        await update.callback_query.answer()
        # Меняем сообщение на кнопку для старта
        keyboard = [
            [InlineKeyboardButton("🔄 Начать снова 🔄", callback_data='restart')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(
            "Если хотите продолжить, нажмите кнопку ниже.",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка в обработчике stop_command: {e}")

async def restart_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик кнопки "Начать снова" после остановки.
    Воссоздаёт поведение команды /start.
    """
    try:
        await start_command(update, context)
    except Exception as e:
        logger.error(f"Ошибка в обработчике restart_command: {e}")

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

        # Обработчики для инлайн-кнопок
        application.add_handler(CallbackQueryHandler(random_command, pattern='random_pose'))
        application.add_handler(CallbackQueryHandler(stop_command, pattern='stop'))
        application.add_handler(CallbackQueryHandler(restart_command, pattern='restart'))

        # Запуск бота
        logger.info("Бот запущен.")
        application.run_polling()

    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
