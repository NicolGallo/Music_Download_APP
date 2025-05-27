import os
import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL
import imageio_ffmpeg

def descargar_audio():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Advertencia", "Por favor, introduce un enlace de YouTube.")
        return

    carpeta = carpeta_destino.get().strip()
    if not carpeta:
        messagebox.showwarning("Advertencia", "Selecciona una carpeta de destino.")
        return

    try:
        os.makedirs(carpeta, exist_ok=True)

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        opciones = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'quiet': False
        }

        with YoutubeDL(opciones) as ydl:
            ydl.download([url])

        messagebox.showinfo("Éxito", "El audio se ha descargado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_destino.set(carpeta)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Descargar audio de YouTube")
ventana.geometry("500x200")
ventana.resizable(False, False)

# Variables
entrada_url = tk.StringVar()
carpeta_destino = tk.StringVar()

# Widgets
tk.Label(ventana, text="Enlace de YouTube:").pack(pady=5)
tk.Entry(ventana, textvariable=entrada_url, width=60).pack()

tk.Label(ventana, text="Carpeta de destino:").pack(pady=5)
frame_carpeta = tk.Frame(ventana)
frame_carpeta.pack()
tk.Entry(frame_carpeta, textvariable=carpeta_destino, width=45).pack(side=tk.LEFT)
tk.Button(frame_carpeta, text="Seleccionar", command=seleccionar_carpeta).pack(side=tk.LEFT, padx=5)

tk.Button(ventana, text="Descargar MP3", command=descargar_audio, bg="#4CAF50", fg="white", width=20).pack(pady=20)

ventana.mainloop()
