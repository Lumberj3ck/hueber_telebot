import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import *

load_dotenv()    

api_token = os.getenv('API_TOKEN')

bot = telebot.TeleBot(api_token)

file_ids = {}
        

@bot.message_handler(commands=['start'])
def start(message):
    content = generate_books_page()
    # content = generate_page_content(1)
    # markup = create_page_markup(1)
    # bot.send_message(message.chat.id, content, reply_markup=markup)
    bot.send_message(message.chat.id, content)


@bot.message_handler(func=lambda message: message.text.startswith('/book'))
def get_lectures_for_book(message):
    book_id = message.text[5:]  # Extract the audio ID from the command
    content = generate_lectures_page(book_id)

    if content:
        bot.reply_to(message, content)
    else:
        bot.reply_to(message, f"Didn't find lectures for given book id")

@bot.message_handler(func=lambda message: message.text.startswith('/audio'))
def handle_audio(message):
    audio_id = message.text[6:]  # Extract the audio ID from the command
    audio = sql_queries.get_audio_by_id(db_name, audio_id)
    # bot.reply_to(message, f"Here's your audio file for ID: {audio_id}")

    if audio:
        if audio_id in file_ids:
            bot.send_audio(chat_id=message.chat.id, audio=file_ids[audio_id])
        else:
            sent_audio = bot.send_audio(chat_id=message.chat.id, audio=open(f"audio_files/{audio[2]}/{audio[1]}", "rb"))
            file_ids[audio_id] = sent_audio.audio.file_id
    else:
        bot.reply_to(message, f"Didn't find audio for id: {audio_id}")

# @bot.message_handler(func=lambda message: message.text.startswith('/lecture'))
# def get_lectures_for_book(message):
#     lecture_id = message.text[8:]  # Extract the audio ID from the command
#     content = generate_audio_page(lecture_id)
#     if content:
#         bot.reply_to(message, content)
#     else:
#         bot.reply_to(message, f"Didn't find audious for given lecture")

@bot.message_handler(func=lambda message: message.text.startswith('/lecture'))
def get_lectures_for_book(message):
    lecture_id = message.text[8:]  # Extract the lecture ID from the command
    page = 1  # Start with the first page
    send_paginated_content(message.chat.id, lecture_id, page)

def send_paginated_content(chat_id, lecture_id, page, message_id=None):
    content, total_pages = generate_audio_page(lecture_id, page)
    if content:
        markup = create_pagination_keyboard(lecture_id, page, total_pages)
        if message_id:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=content, reply_markup=markup)
        else:
            sent_message = bot.send_message(chat_id, content, reply_markup=markup)
            return sent_message.message_id
    else:
        bot.send_message(chat_id, "Didn't find audios for the given lecture")

def create_pagination_keyboard(lecture_id, current_page, total_pages):
    markup = InlineKeyboardMarkup()
    buttons = []

    if current_page > 1:
        buttons.append(InlineKeyboardButton("Previous", callback_data=f"lectures_page_{lecture_id}_{current_page-1}"))
    
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton("Next", callback_data=f"lectures_page_{lecture_id}_{current_page+1}"))
    
    markup.row(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('lectures_page_'))
def callback_query(call):
    _, _, lecture_id, page = call.data.split('_')
    page = int(page)
    send_paginated_content(call.message.chat.id, lecture_id, page, call.message.message_id)
    bot.answer_callback_query(call.id)


bot.polling()
