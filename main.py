from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from config import TOKEN


PRODUCTS_DICT = {
    'one': {
        'name': 'One',
        'image_path': 'images/one/pop.jpg',
        'description': 'Description for One',
        'link': 'http://example.com/one',
    },
    'two': {
        'name': 'Two',
        'image_path': 'images/two/pop.jpg',
        'description': 'Description for Two',
        'link': 'http://example.com/two',
    },
    'three': {
        'name': 'Three',
        'image_path': 'images/three/pop.jpg',
        'description': 'Description for Three',
        'link': 'http://example.com/three',
    },
}

# Обработчик команды /start
def start(update, context):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"Привет, {user.first_name}! Я бот. Чем могу помочь?",
                             reply_markup=get_main_keyboard())

# Получение основной клавиатуры
def get_main_keyboard():
    keyboard = [[KeyboardButton("Ассортимент", callback_data='assortment')]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def handle_text(update, context):
    text = update.message.text
    if text == "Ассортимент":
        assortment(update, context)

def assortment(update, context):
    keyboard = get_categories_keyboard()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Выберите категорию:",
        reply_markup=keyboard
    )

def handle_category_selection(update, context):
    query = update.callback_query
    category = query.data
    product_info = PRODUCTS_DICT.get(category)

    if product_info:
        context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=open(product_info['image_path'], 'rb'),
            caption=f"{product_info['name']}\n{product_info['description']}\nLink: {product_info['link']}"
        )
    else:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Произошла ошибка. Пожалуйста, попробуйте еще раз."
        )

def get_categories_keyboard():
    keyboard = [
        [KeyboardButton("One", callback_data='one')],
        [KeyboardButton("Two", callback_data='two')],
        [KeyboardButton("Three", callback_data='three')],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # # Обработчик кнопок категорий
    # dp.add_handler(CallbackQueryHandler())

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
