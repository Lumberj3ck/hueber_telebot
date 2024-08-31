import os
from sql import sql_queries
from dotenv import load_dotenv

load_dotenv()    
ITEMS_PER_PAGE = 5
db_name = os.getenv('DB')

def generate_books_page():
    content = ''
    books = sql_queries.get_all_books(db_name)
    for book in books:
        content += f'{book[0]}  {book[1]} \n /book{book[0]} \n'
    return content

def generate_lectures_page(book_id, page, current_page_type):
    if current_page_type == 'workbook':
        lectures = sql_queries.get_workbook_lectures_by_book_id(db_name, book_id)
    else:
        lectures = sql_queries.get_lectures_by_book_id(db_name, book_id)

    # first_workbook = True
    if lectures:
        total_pages = (len(lectures) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        start_idx = (page - 1) * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_lectures = lectures[start_idx:end_idx]

        content = f'{current_page_type.capitalize()} {lectures[0][2]} (Page {page}/{total_pages}) \n\n'
        for lecture in page_lectures:
            # if first_workbook and lecture[3] == "workbook":
            #     content += "Workbook Lectures \n\n" 
            #     first_workbook = False
            content += f"Lecture 0{lecture[1]} \n /lecture{lecture[0]} \n\n"
        return content, total_pages
    else:
        return None, 0


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
