from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import os
import uuid

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 🌐 דף אתר
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Audio Downloader</title>
        </head>
        <body style="font-family: Arial; text-align:center; margin-top:50px;">
            <h1>🎧 Audio Downloader</h1>

            <input id="url" style="width:300px; padding:10px;" placeholder="Paste video URL" />
            <br><br>

            <button onclick="download()" style="padding:10px 20px;">
                Download
            </button>

            <script>
                function download() {
                    const url = document.getElementById('url').value;
                    window.location.href = '/download?url=' + encodeURIComponent(url);
                }
            </script>
        </body>
    </html>
    """

# 📥 API להורדה
@app.get("/download")
def download(url: str = Query(...)):
    file_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{file_id}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return FileResponse(output_path, media_type="audio/mpeg", filename="audio.mp3")
