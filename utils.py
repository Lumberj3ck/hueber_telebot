import os
from sql import sql_queries
from dotenv import load_dotenv

load_dotenv()    
db_name = os.getenv('DB')

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

# def generate_audio_page(lecture_id):
#     audios = sql_queries.get_audios_by_lecture_id(db_name, lecture_id)
#     if audios:
#         content = f'Lecture {audios[0][2]} from {audios[0][3]} \n\n'
#         for audio in audios:
#             # don't need audio path
#             # content += f"Audio 0{audio[4]} \n /audio{audio[0]} \n\n"
#             content += f"{audio[5]} \n /audio{audio[0]} \n\n"
#         return content
#     else:
#         return None
        
ITEMS_PER_PAGE = 5

def generate_audio_page(lecture_id, page):
    audios = sql_queries.get_audios_by_lecture_id(db_name, lecture_id)
    # print(audios)
    if audios:
        total_pages = (len(audios) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        start_idx = (page - 1) * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_audios = audios[start_idx:end_idx]

        book_type = "Workbook" if audios[0][7] == 'workbook' else "Kursbook"
        content = f'{book_type} lecture {audios[0][6]} from {audios[0][3]} (Page {page}/{total_pages})\n\n'
        for audio in page_audios:
            content += f"{audio[5]}\n/audio{audio[0]}\n\n"
        return content, total_pages
    else:
        return None, 0
