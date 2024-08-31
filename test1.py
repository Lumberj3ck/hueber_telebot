import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sql import sql_queries


api_token = '7228889532:AAGefcjfSB5zxerj2GDqeIbEF6OsI1M5LBg'


bot = telebot.TeleBot(api_token)


def create_inline_keyboard():
    markup = InlineKeyboardMarkup()
    
    # Add buttons to the keyboard
    markup.row(InlineKeyboardButton("Option 1", callback_data="option1"),
               InlineKeyboardButton("Option 2", callback_data="option2"))
    
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "option1":
        bot.edit_message_text(chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=call.data,
                        reply_markup=create_inline_keyboard()) 
        bot.answer_callback_query(call.id, "You selected Option 1")
    elif call.data == "option2":
        bot.answer_callback_query(call.id, "You selected Option 2"  )


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""", reply_markup=create_inline_keyboard())


@bot.message_handler(func=lambda message: True)
def text_handler(message):
    book_query = message.text
    sql_queries.get_lectures_by_book_name("hueber_media.db", book_query)
    bot.reply_to(message, "Your message is " + message.text)

@bot.message_handler(func=lambda message: True)
def text_handler(message):
    id = message.text.split("/download")

    bot.reply_to(message, "Your message is " + message.text)

bot.infinity_polling()
