from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import os
import uuid
import threading
import time

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 🧹 ניקוי אוטומטי (כל 10 דקות)
def cleanup():
    while True:
        now = time.time()
        for file in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, file)
            if os.path.isfile(path):
                if now - os.path.getmtime(path) > 600:
                    os.remove(path)
        time.sleep(300)

threading.Thread(target=cleanup, daemon=True).start()


# 🌐 UI עם loading
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Audio Downloader</title>
        <style>
            body { font-family: Arial; text-align:center; margin-top:80px; }
            input { width:320px; padding:10px; }
            button { padding:10px 20px; cursor:pointer; }
            #status { margin-top:20px; font-weight:bold; }
        </style>
    </head>

    <body>
        <h1>🎧 Audio Downloader</h1>

        <input id="url" placeholder="Paste YouTube URL" />
        <br><br>

        <button onclick="download()">Download</button>

        <div id="status"></div>

        <script>
            function download() {
                const url = document.getElementById('url').value;
                const status = document.getElementById('status');

                if (!url) {
                    status.innerText = "❌ Please paste a link";
                    return;
                }

                status.innerText = "⏳ Downloading... please wait";

                window.location.href =
                    '/download?url=' + encodeURIComponent(url);
            }
        </script>
    </body>
    </html>
    """


# 📥 API יציב יותר
@app.get("/download")
def download(url: str = Query(...)):

    file_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{file_id}.mp3"

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "noplaylist": True,
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(output_path):
            return {"error": "File not created"}

        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename="audio.mp3"
        )

    except Exception as e:
        return {"error": str(e)}
