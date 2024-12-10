from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, ContextTypes

TOKEN = '7601748735:AAEe3aIX8OSBH4-W-0vz3_IB_SEhg30TmRI'

# Состояния игры
FIRST_TASK, SECOND_TASK, THIRD_TASK, FOURTH_TASK = range(4)

# Начало игры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Добро пожаловать в квест! Ваше первое задание: "Пробуждение магической печати".\n\n'
        'Вы попадаете в древний зал, в центре которого расположена светящаяся магическая печать. '
        'Чтобы активировать её и открыть путь вперёд, нужно выбрать правильное заклинание.\n\n'
        'Выберите заклинание:',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Люмос', callback_data='FIRST_1')],
            [InlineKeyboardButton('Алохомора', callback_data='FIRST_2')],
            [InlineKeyboardButton('Эксспекто Патронум', callback_data='FIRST_3')],
            [InlineKeyboardButton('Авада Кедавра', callback_data='FIRST_4')]
        ])
    )
    return FIRST_TASK

# Первое задание с описанием
async def first_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'FIRST_2':
        await query.edit_message_text(
            text="Печать активируется, дверь открыта! Вы переходите к следующему заданию.\n\n"
            "Описание: Вы выбрали заклинание 'Алохомора', которое оказалось верным. "
            "Печать излучает яркий свет, и перед вами открывается проход. Вы чувствуете, что вы на правильном пути."
        )
        return await second_task(update, context)
    else:
        await query.edit_message_text(
            text="Неверное заклинание! Попробуйте ещё раз.\n\n"
            "Описание: Заклинание не сработало. Печать мигает, но не реагирует на вашу попытку. "
            "Подумайте, какое заклинание могло бы подойти для активации магической силы."
        )
        return FIRST_TASK

# Второе задание с описанием
async def second_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text(
        "Новое задание: 'Сопротивление магическим ловушкам'.\n\n"
        "В этой комнате вы видите магическую ловушку, активирующуюся при любом движении. "
        "Вам нужно выбрать заклинание, которое временно её обезвредит. Ошибка может привести к активизации ловушки!\n\n"
        "Выберите заклинание:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Петрификус Тоталус', callback_data='SECOND_1')],
            [InlineKeyboardButton('Левикорпус', callback_data='SECOND_2')],
            [InlineKeyboardButton('Люмос', callback_data='SECOND_3')],
            [InlineKeyboardButton('Авада Кедавра', callback_data='SECOND_4')]
        ])
    )
    return SECOND_TASK

async def second_task_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'SECOND_1':
        await query.edit_message_text(
            text="Ловушка временно замораживается. Вы успеваете пройти дальше!\n\n"
            "Описание: Вы произносите 'Петрификус Тоталус', и ловушка замораживается, давая вам возможность безопасно продвинуться вперёд. "
            "Теперь вы готовы к следующему испытанию."
        )
        return await third_task(update, context)
    else:
        await query.edit_message_text(
            text="Заклинание не сработало. Попробуйте ещё раз.\n\n"
            "Описание: Вы пробуете другое заклинание, но ловушка не реагирует должным образом. Подумайте, какое заклинание подходит для защиты от ловушки."
        )
        return SECOND_TASK

# Третье задание с описанием
async def third_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text(
        "Новое задание: 'Нахождение скрытого объекта'.\n\n"
        "В комнате с блестящими кристаллами находится один ключевой предмет, который открывает дверь в следующую часть зала. "
        "Вы должны использовать заклинание, чтобы найти его среди множества похожих кристаллов.\n\n"
        "Выберите заклинание:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Стомпор', callback_data='THIRD_1')],
            [InlineKeyboardButton('Люмос', callback_data='THIRD_2')],
            [InlineKeyboardButton('Редукто', callback_data='THIRD_3')],
            [InlineKeyboardButton('Империус', callback_data='THIRD_4')]
        ])
    )
    return THIRD_TASK

async def third_task_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'THIRD_3':
        await query.edit_message_text(
            text="Заклинание 'Редукто' сработало! Вы нашли нужный кристалл.\n\n"
            "Описание: Вы произносите 'Редукто', и с помощью разрушительной силы разрушаете всё лишнее, оставляя только ключевой кристалл. "
            "Вы берёте его и готовитесь к последнему заданию."
        )
        return await fourth_task(update, context)
    else:
        await query.edit_message_text(
            text="Попробуйте ещё раз.\n\n"
            "Описание: Заклинание не позволило найти нужный кристалл. Постарайтесь выбрать что-то другое."
        )
        return THIRD_TASK

# Четвертое задание с описанием
async def fourth_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text(
        "Последнее задание: 'Сохранение памяти'.\n\n"
        "Вы видите духа, охраняющего воспоминания о важной информации. "
        "Чтобы получить эту информацию, нужно использовать правильное заклинание. Неверное действие может уничтожить воспоминания.\n\n"
        "Выберите заклинание:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Петрификус Тоталус', callback_data='FOURTH_1')],
            [InlineKeyboardButton('Империус', callback_data='FOURTH_2')],
            [InlineKeyboardButton('Люмос', callback_data='FOURTH_3')],
            [InlineKeyboardButton('Авада Кедавра', callback_data='FOURTH_4')]
        ])
    )
    return FOURTH_TASK

async def fourth_task_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'FOURTH_1':
        await query.edit_message_text(
            text="Поздравляем! Вы успешно завершили квест.\n\n"
            "Описание: Вы произносите 'Петрификус Тоталус', и дух замораживается, предоставляя вам возможность забрать важные воспоминания. "
            "Вы завершили квест и можете гордиться своей победой!"
        )
        return ConversationHandler.END
    else:
        await query.edit_message_text(
            text="Попробуйте ещё раз.\n\n"
            "Описание: Заклинание не сработало, и дух начинает исчезать. Вы должны быть осторожны и выбрать другое заклинание."
        )
        return FOURTH_TASK

# Основная функция
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_TASK: [CallbackQueryHandler(first_task, pattern='^FIRST_')],
            SECOND_TASK: [CallbackQueryHandler(second_task_response, pattern='^SECOND_')],
            THIRD_TASK: [CallbackQueryHandler(third_task_response, pattern='^THIRD_')],
            FOURTH_TASK: [CallbackQueryHandler(fourth_task_response, pattern='^FOURTH_')],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
