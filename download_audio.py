import yt_dlp

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    print("מתחיל בהורדה...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("ההורדה וההמרה הסתיימו בהצלחה!")
    except Exception as e:
        print(f"אירעה שגיאה: {e}")

video_url = input("אנא הכנס את קישור ה-YouTube: ")
download_audio(video_url)
