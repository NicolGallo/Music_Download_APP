import os
from yt_dlp import YoutubeDL
import imageio_ffmpeg

def descargar_mp3(url, carpeta_destino, calidad="192", progreso_callback=None):
    os.makedirs(carpeta_destino, exist_ok=True)
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    info_capturada = {}

    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': calidad,
        }],
        'progress_hooks': [progreso_callback] if progreso_callback else [],
        'quiet': True,
        'noprogress': True,
        'skip_download': False,
        'forcejson': True,
        'extract_flat': False,
        'default_search': 'auto'
    }

    with YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        info_capturada = {
            "titulo": info.get("title", "Desconocido"),
            "duracion": info.get("duration", 0),
            "tamanio": info.get("filesize_approx", 0),
            "url": info.get("webpage_url", url)
        }

    return info_capturada
