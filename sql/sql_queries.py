import sqlite3


def get_cursor(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    return cursor, conn

def get_lectures_by_book_name(db_path, book_name):
    # Connect to the SQLite database

    cursor, conn = get_cursor(db_path)

    # SQL query to select lectures associated with the given book name
    query = '''
    SELECT l.id, l.number, b.name AS book_name
    FROM lecture l
    JOIN book b ON l.content_id = b.id
    WHERE l.content_type = 'book' AND b.name = ?
    ORDER BY l.number
    '''

    # Execute the query with the book name as a parameter
    cursor.execute(query, (book_name,))

    # Fetch all the results
    lectures = cursor.fetchall()

    # Close the database connection
    conn.close()

    return lectures

def get_lectures_by_book_id(db_path, book_id):

    cursor, conn = get_cursor(db_path)

    query = '''
    SELECT l.id, l.number, b.name, l.content_type AS book_name
    FROM lecture l
    JOIN book b ON l.content_id = b.id
    WHERE b.id = ?
    ORDER BY l.content_type, l.number
    '''

    cursor.execute(query, (book_id, ))

    # Fetch all the results
    lectures = cursor.fetchall()

    # Close the database connection
    conn.close()

    return lectures
    
def get_audios_by_lecture_id(db_path, lecture_id):

    cursor, conn = get_cursor(db_path)

    query = '''
    SELECT a.id, a.path, l.id, b.name, a.number, a.title  FROM audio a
    JOIN lecture l ON a.lecture_id = l.id
    JOIN book b ON l.content_id = b.id
    WHERE l.id = ?
    ORDER BY a.id
    '''

    cursor.execute(query, (lecture_id, ))

    # Fetch all the results
    audios = cursor.fetchall()

    # Close the database connection
    conn.close()

    return audios

def get_audio_by_id(db_path, audio_id):

    cursor, conn = get_cursor(db_path)

    query = '''
    SELECT a.id, a.path, b.name from audio a
    JOIN lecture l ON l.id = a.lecture_id
    JOIN book b ON b.id = l.content_id
    WHERE a.id = ?
    '''

    cursor.execute(query, (audio_id, ))

    # Fetch all the results
    audio = cursor.fetchone()

    # Close the database connection
    conn.close()

    return audio

def get_all_books(db_path):

    cursor, conn = get_cursor(db_path)

    query = '''
    SELECT * FROM book
    '''

    cursor.execute(query)

    # Fetch all the results
    books = cursor.fetchall()

    # Close the database connection
    conn.close()

    return books

# print(get_lectures_by_book_name('hueber_media.db', 'Schritte plus neu'))