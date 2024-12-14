import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Функция для загрузки заданий из файла zad.txt
def load_tasks():
    with open('zad.txt', 'r', encoding='utf-8') as file:
        tasks = file.readlines()
    return [task.strip() for task in tasks]  # Убираем лишние пробелы и символы новой строки

# Функция для отправки 5 случайных заданий
async def random_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()  # Загружаем все задания из файла
    random_tasks = random.sample(tasks, 5)  # Рандомно выбираем 5 заданий

    # Отправляем все задания пользователю
    response = '\n'.join(random_tasks)
    await update.message.reply_text(response)

# Функция для замены текста на выполнение команды /tasks
async def text_to_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Выполнение команды /tasks
    await random_tasks(update, context)

def main():
    # Токен вашего бота
    token = '7601748735:AAEe3aIX8OSBH4-W-0vz3_IB_SEhg30TmRI'  # Замените на токен вашего бота

    # Создаем объект Application для взаимодействия с Telegram API
    application = Application.builder().token(token).build()

    # Регистрация обработчика команды /tasks
    application.add_handler(CommandHandler('tasks', random_tasks))

    # Регистрация обработчика текстовых сообщений (выполняет команду /tasks)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_tasks))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
