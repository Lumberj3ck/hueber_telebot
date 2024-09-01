import os
import re
import sqlite3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def get_mp3_title(file_path):
    try:
        # Load the MP3 file
        audio = MP3(file_path, ID3=ID3)
        
        # Check if the file has an ID3 tag
        if audio.tags:
            # Try to get the title from the ID3 tag
            title = audio.tags.get('TIT2')
            if title:
                return title.text[0]
    
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_info_from_filename(filename, directory):
    pattern = r'(\d+)_(\w+)?_L(\d+)_(\d+)\.mp3'
    match = re.match(pattern, filename)
    if match:
        book_id, book_type, lecture_number, audio_number = match.groups()
        path_to_file = os.path.join(directory, filename)
        title = get_mp3_title(path_to_file)
        return {
            'book_id': int(book_id),
            'title': title, 
            'content_type': 'workbook' if book_type == "AB" else 'book',
            'lecture_number': int(lecture_number),
            'path': filename,
            'audio_number': audio_number
        }
    return None

def insert_data(conn, data):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM book WHERE name = ?
    ''', (data['book_name'], ))

    book = cursor.fetchone()
    if book:
        content_id = book[0]
    else:
        cursor.execute('''
            INSERT OR IGNORE INTO book (name) VALUES (?)
        ''', (data['book_name'], ) )

        content_id = cursor.lastrowid


    cursor.execute('''
        SELECT id FROM lecture
        WHERE number = ? AND content_type = ? AND content_id = ?
    ''', (data['lecture_number'], data['content_type'], content_id))
    
    result = cursor.fetchone()
    if result:
        lecture_id = result[0]
    else:
        cursor.execute('''
            INSERT INTO lecture (number, content_type, content_id)
            VALUES (?, ?, ?)
        ''', (data['lecture_number'], data['content_type'], content_id))
        lecture_id = cursor.lastrowid

    cursor.execute('''
        SELECT * FROM audio WHERE path = ? AND lecture_id = ? AND number = ?
    ''', (data['path'], lecture_id, data['audio_number']))

    audio = cursor.fetchone()

    if not audio:
        cursor.execute('''
            INSERT INTO audio (path, lecture_id, number, title) VALUES (?, ?, ?, ?)
        ''', (data['path'], lecture_id, data['audio_number'], data['title']))

    conn.commit()

def process_files(directory, book_name, db_path):
    conn = sqlite3.connect(db_path)

    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            data = extract_info_from_filename(filename, directory)
            if data:
                data['book_name'] = book_name
                insert_data(conn, data)
            else:
                print(f"Skipping file with invalid format: {filename}")

    conn.close()

book_directory = 'Schritte_plus_neu_2_a2.2'
path_to_files = os.path.join('audio_files', book_directory)
process_files(path_to_files, book_directory, 'hueber_media.db')
