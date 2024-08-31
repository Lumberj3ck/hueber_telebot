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

print(get_mp3_title(r"C:\Users\Lumberjack\code\hueber_telebot\audio_files\Schritte_plus_neu_a1.1\301081_AB_L01_01.mp3"))