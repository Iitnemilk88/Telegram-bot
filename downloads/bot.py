from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random

# Идеи для свиданий
date_ideas = [
    "Ужин при свечах дома",
    "Прогулка по парку с пикником",
    "Совместный мастер-класс по кулинарии",
    "Выезд на природу с палатками",
    "Посещение музея или выставки"
]

# Игры для пар
games = [
    "Игра в вопросы: Что бы ты выбрал? (например, море или горы?)",
    "Угадай предпочтение партнера: что он предпочитает - кошек или собак?",
    "Напишите друг другу письмо, как в старые времена"
]

# Функция для команды /date
def date(update: Update, context: CallbackContext) -> None:
    idea = random.choice(date_ideas)
    update.message.reply_text(f"Вот идея для свидания: {idea}")

# Функция для команды /game
def game(update: Update, context: CallbackContext) -> None:
    challenge = random.choice(games)
    update.message.reply_text(f"Вот игра для вас: {challenge}")

# Основная функция
def main() -> None:
    # Вставьте сюда ваш токен
    TOKEN = '2056709740:AAFnVh_aQmQB_MirfS_T02txVg53MmzQnJE'  
    # Здесь должен быть реальный токен, полученный от BotFather

    # Создаем объект бота
    updater = Updater(TOKEN)

    # Получаем диспетчера
    dispatcher = updater.dispatcher

    # Добавляем обработчики команд
    dispatcher.add_handler(CommandHandler("date", date))
    dispatcher.add_handler(CommandHandler("game", game))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
