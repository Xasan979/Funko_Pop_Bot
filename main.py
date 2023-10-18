from telegram import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import TOKEN

# Обновленная структура PRODUCTS_DICT
PRODUCTS_DICT = {
    'one': [
        {
            'name': 'Исщадье',
            'image_path': 'images/one/1.png',
            'description': 'Четкая фигурка, лучше чем нарды, залетай покупай !!!',
            'link': 'https://www.avito.ru',
        },
        {
            'name': 'Джек2',
            'image_path': 'images/one/2.png',
            'description': 'ехохо и бутылка рома',
            'link': 'https://www.avito.ru',
        },
        {
            'name': 'Джек3',
            'image_path': 'images/one/3.png',
            'description': 'КАПИТАН - капитан ждек воробей',
            'link': 'https://www.avito.ru',
        },
    ],
}

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
    keyboard = [[KeyboardButton("Категории товаров", callback_data='assortment')]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Обработчик команды /one
def one(update, context):
    product_info_list = PRODUCTS_DICT.get('one', [])

    if product_info_list:
        for product_info in product_info_list:
            image_path = product_info.get('image_path')
            image = open(image_path, 'rb') if image_path else None

            caption = f"Информация о продукте {product_info['name']}:\n" \
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

# Обработчик текстовых сообщений для вывода категорий товаров
def assortment(update, context):
    keyboard = get_categories_keyboard()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Выберите категорию:",
        reply_markup=keyboard
    )

# Функция для получения клавиатуры с категориями товаров
def get_categories_keyboard():
    keyboard = [[KeyboardButton("/One", callback_data='one')]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция для обработки нажатия кнопок
def button_click(update, context):
    query = update.callback_query
    if query.data == 'one':
        one(update, context)

# Функция для запуска бота
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Обработчик команды /one
    dp.add_handler(CommandHandler("one", one))

    # Обработчик для нажатия кнопок
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
