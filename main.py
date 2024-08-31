import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sql import sql_queries

load_dotenv()    

api_token = os.getenv('API_TOKEN')

bot = telebot.TeleBot(api_token)
db_name = os.getenv('DB')

file_ids = {}

def generate_books_page():
    content = ''
    books = sql_queries.get_all_books(db_name)
    for book in books:
        content += f'{book[0]}  {book[1]} \n /book{book[0]} \n'
    return content

def generate_lectures_page(book_id):
    lectures = sql_queries.get_lectures_by_book_id(db_name, book_id)
    first_workbook = True
    if lectures:
        content = f'{lectures[0][2]} \n\n'
        for lecture in lectures:
            if first_workbook and lecture[3] == "workbook":
                content += "Workbook Lectures \n\n" 
                first_workbook = False
            content += f"Lecture 0{lecture[1]} \n /lecture{lecture[0]} \n\n"
        return content
    else:
        return None

def generate_audio_page(lecture_id):
    audios = sql_queries.get_audios_by_lecture_id(db_name, lecture_id)
    if audios:
        content = f'Lecture {audios[0][2]} from {audios[0][3]} \n\n'
        for audio in audios:
            # don't need audio path
            # content += f"Audio 0{audio[4]} \n /audio{audio[0]} \n\n"
            content += f"{audio[5]} \n /audio{audio[0]} \n\n"
        return content
    else:
        return None
        

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

@bot.message_handler(func=lambda message: message.text.startswith('/lecture'))
def get_lectures_for_book(message):
    lecture_id = message.text[8:]  # Extract the audio ID from the command
    content = generate_audio_page(lecture_id)
    if content:
        bot.reply_to(message, content)
    else:
        bot.reply_to(message, f"Didn't find audious for given lecture")

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

@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def callback_query(call):
    page = int(call.data.split('_')[1])
    content = generate_page_content(page)
    markup = create_page_markup(page)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=content,
                          reply_markup=markup)
    bot.answer_callback_query(call.id)

bot.polling()
