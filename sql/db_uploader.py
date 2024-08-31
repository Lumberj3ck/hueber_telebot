import os
import re
import sqlite3

def extract_info_from_filename(filename):
    pattern = r'(\d+)_(\w+)?_L(\d+)_(\d+)\.mp3'
    match = re.match(pattern, filename)
    if match:
        book_id, book_type, lecture_number, audio_number = match.groups()
        return {
            'book_id': int(book_id),
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
            INSERT INTO audio (path, lecture_id, number) VALUES (?, ?, ?)
        ''', (data['path'], lecture_id, data['audio_number']))

    conn.commit()

def process_files(directory, book_name, db_path):
    conn = sqlite3.connect(db_path)

    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            data = extract_info_from_filename(filename)
            if data:
                data['book_name'] = book_name
                insert_data(conn, data)
            else:
                print(f"Skipping file with invalid format: {filename}")

    conn.close()

book_directory = 'Schritte_plus_neu_a1.1'
path_to_files = os.path.join('audio_files', book_directory)
process_files(path_to_files, book_directory, 'hueber_media.db')