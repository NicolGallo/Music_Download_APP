import os
from yt_dlp import YoutubeDL
import imageio_ffmpeg

def descargar_mp3(url, carpeta_destino, calidad="192", progreso_callback=None):
    os.makedirs(carpeta_destino, exist_ok=True)
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    info_capturada = {}

    opciones = {
        'format': 'best[ext=mp4]/best[ext=webm]/best',  # Evita HLS
        'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': calidad,
        }],
        'progress_hooks': [progreso_callback] if progreso_callback else [],
        'quiet': False,
        'no_warnings': False,
        'socket_timeout': 30,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        'extractor_args': {'youtube': {'skip': ['hls']}},  # Salta formatos HLS
        'allow_unplayable_formats': False,
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