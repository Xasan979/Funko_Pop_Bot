from telegram import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from data import *

# Обработчик команды /start
def start(update, context):
    user = update.message.from_user
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Привет, {user.first_name}! Я бот. Чем могу помочь?",
        reply_markup=get_main_keyboard()
    )

# Обработчик текстовых сообщений
def handle_text(update, context):
    text = update.message.text
    if text == "Категории товаров":
        assortment(update, context)

# Получение основной клавиатуры
def get_main_keyboard():
    keyboard = [[KeyboardButton("Категории товаров", callback_data='assortment')],
                [KeyboardButton("/Акции", callback_data='assortment')],
                [KeyboardButton("Предзаказы", callback_data='assortment')],
                [KeyboardButton("Связаться с нами", callback_data='assortment')]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Обработчик текстовых сообщений для вывода категорий товаров
def assortment(update, context):
    keyboard = get_categories_keyboard()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Выберите категорию:",
        reply_markup=keyboard
    )

def command_processing(update, context, product_key):  # обработчик команд
    product_info_list = PRODUCTS_DATA.get(product_key, [])

    if product_info_list:
        for product_info in product_info_list:
            image_path = product_info.get('image_path')
            image = open(image_path, 'rb') if image_path else None

            caption = f"{product_info['name']} :\n" \
                      f"{product_info['description']}\n" \
                      f"Ссылка: {product_info['link']}"

            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=image,
                caption=caption
            )

            if image:
                image.close()
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Продукт не найден.",
        )

# Обработчик команды /one
def one(update, context):
    command_processing(update, context, 'one')

# Обработчик команды /two
def two(update, context):
    command_processing(update, context, 'two')

# Обработчик команды /three
def three(update, context):
    command_processing(update, context, 'three')

# Обработчик команды /stocks
def stocks(update, context):
    command_processing(update, context, 'stocks')


# Функция для получения клавиатуры с категориями товаров
def get_categories_keyboard():
    keyboard = [
        [KeyboardButton("/One", callback_data='one')],
        [KeyboardButton("/Two", callback_data='two')],
        [KeyboardButton("/Three", callback_data='three')],
        [KeyboardButton("/Menu", callback_data='menu')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция для обработки нажатия кнопок
def button_click(update, context):
    query = update.callback_query
    if query.data in ['one', 'two', 'three']:
        # Отправляем команду в чат
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=query.data  # отправляем сам query.data без добавления /
        )
    elif query.data == 'menu':
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text="Возвращаемся в главное меню.",
            reply_markup=get_main_keyboard()
        )
    elif query.data == 'stocks':
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text="Акции на товары:",
            reply_markup=get_main_keyboard()
        )
    else:
        # Ваша логика обработки других кнопок
        pass


# Добавлен обработчик команды /меню
def get_main_menu(update, context):
    keyboard = get_main_keyboard()
    user = update.message.from_user
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Возвращаемся в главное меню, {user.first_name}!",
        reply_markup=keyboard
    )

# Функция для запуска бота
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Добавлен обработчик для команды /get_main_menu
    dp.add_handler(CommandHandler("menu", get_main_menu))

    # Обработчик команды /one
    dp.add_handler(CommandHandler("one", one))

    # Обработчик команды /two
    dp.add_handler(CommandHandler("two", two))

    # Обработчик команды /three
    dp.add_handler(CommandHandler("three", three))

    # Обработчик команды /stocks
    dp.add_handler(CommandHandler("stocks", stocks))

    # Обработчик для нажатия кнопок
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


"""Лучший вариант реализации , без возврата в меню"""

# from telegram import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
# from data import *
#
#
# # Обработчик команды /start
# def start(update, context):
#     user = update.message.from_user
#     context.bot.send_message(
#         chat_id=update.message.chat_id,
#         text=f"Привет, {user.first_name}! Я бот. Чем могу помочь?",
#         reply_markup=get_main_keyboard()
#     )
#
#
# # Обработчик текстовых сообщений
# def handle_text(update, context):
#     text = update.message.text
#     if text == "Категории товаров":
#         assortment(update, context)
#
#
# # Получение основной клавиатуры
# def get_main_keyboard():
#     keyboard = [[KeyboardButton("Категории товаров", callback_data='assortment')],
#                 [KeyboardButton("Акции", callback_data='assortment')],
#                 [KeyboardButton("Предзаказы", callback_data='assortment')],
#                 [KeyboardButton("Связаться с нами", callback_data='assortment')]]
#     return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#
# # Обработчик текстовых сообщений для вывода категорий товаров
# def assortment(update, context):
#     keyboard = get_categories_keyboard()
#     context.bot.send_message(
#         chat_id=update.message.chat_id,
#         text="Выберите категорию:",
#         reply_markup=keyboard
#     )
#
#
# def command_processing(update, context, product_key):                # обработчик команд
#     product_info_list = PRODUCTS_DATA.get(product_key, [])
#
#     if product_info_list:
#         for product_info in product_info_list:
#             image_path = product_info.get('image_path')
#             image = open(image_path, 'rb') if image_path else None
#
#             caption = f"{product_info['name']} :\n" \
#                       f"{product_info['description']}\n" \
#                       f"Ссылка: {product_info['link']}"
#
#             context.bot.send_photo(
#                 chat_id=update.message.chat_id,
#                 photo=image,
#                 caption=caption
#             )
#
#             if image:
#                 image.close()
#     else:
#         context.bot.send_message(
#             chat_id=update.message.chat_id,
#             text="Продукт не найден.",
#         )
#
#
# # Обработчик команды /one
# def one(update, context):
#     command_processing(update, context, 'one')
#
#
# # Обработчик команды /two
# def two(update, context):
#     command_processing(update, context, 'two')
#
#
# # Обработчик команды /three
# def three(update, context):
#     command_processing(update, context, 'three')
#
#
# # Функция для получения клавиатуры с категориями товаров
# def get_categories_keyboard():
#     keyboard = [[KeyboardButton("/One", callback_data='one')],
#                 [KeyboardButton("/Two", callback_data='two')],
#                 [KeyboardButton("/Three", callback_data='three')],
#                 [KeyboardButton("Меню", callback_data='get_main_menu')]]
#     return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#
#
# # Функция для обработки нажатия кнопок
# def button_click(update, context):
#     query = update.callback_query
#     if query.data == 'one':
#         one(update, context)
#     elif query.data == 'two':
#         two(update, context)
#     elif query.data == 'three':
#         three(update, context)
#     elif query.data == 'get_main_menu':
#         context.bot.send_message(
#             chat_id=update.callback_query.from_user.id,
#             text="Возвращаемся в главное меню.",
#             reply_markup=get_main_keyboard()
#         )
#     else:
#         # Ваша логика обработки других кнопок
#         pass
#
# # Обработчик команды /get_main_keyboard
# def get_main_menu(update, context):
#     user = update.message.from_user
#     context.bot.send_message(
#         chat_id=update.message.chat_id,
#         text=f"Возвращаемся в главное меню, {user.first_name}!",
#         reply_markup=get_main_keyboard()
#     )
#
# # Функция для запуска бота
# def main():
#     updater = Updater(token=TOKEN, use_context=True)
#     dp = updater.dispatcher
#
#     # Обработчик команды /start
#     dp.add_handler(CommandHandler("start", start))
#
#     # Обработчик текстовых сообщений
#     dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
#
#     # Добавьте обработчик для команды /get_main_keyboard
#     dp.add_handler(CommandHandler("get_main_keyboard", get_main_menu))
#
#     # Обработчик команды /one
#     dp.add_handler(CommandHandler("one", one))
#
#     # Обработчик команды /two
#     dp.add_handler(CommandHandler("two", two))
#
#     # Обработчик команды /three
#     dp.add_handler(CommandHandler("three", three))
#
#     # # Обработчик для нажатия кнопок
#     # dp.add_handler(CallbackQueryHandler(button_click))
#
#     updater.start_polling()
#     updater.idle()
#
#
# if __name__ == "__main__":
#     main()
