import customtkinter as ctk
from tkinter import filedialog
from core.downloader import descargar_mp3
from core.utils import guardar_en_historial

def iniciar_gui():
    def progreso_hook(d):
        if d['status'] == 'downloading':
            porcentaje = d.get('_percent_str', '0.0%').strip().replace('%', '')
            try:
                progreso.set(float(porcentaje))
            except ValueError:
                progreso.set(0)
        elif d['status'] == 'finished':
            progreso.set(100)

    def descargar():
        url = entrada_url.get().strip()
        carpeta = carpeta_destino.get().strip()
        calidad = calidad_var.get()
        log_textbox.delete("0.0", ctk.END)

        if not url or not carpeta:
            estado.set("❌ Faltan datos.")
            return

        try:
            estado.set("⏳ Descargando...")
            progreso.set(0)
            ventana.update_idletasks()
            info = descargar_mp3(url, carpeta, calidad, progreso_hook)

            # Formateo del log
            duracion_seg = info.get("duracion", 0)
            duracion_str = f"{duracion_seg//60}:{duracion_seg%60:02d} min"
            tamanio_mb = info.get("tamanio", 0) / 1024 / 1024
            texto_log = (
                f"✅ Título: {info.get('titulo')}\n"
                f"🕒 Duración: {duracion_str}\n"
                f"💾 Tamaño estimado: {tamanio_mb:.2f} MB\n"
                f"🔗 URL: {info.get('url')}\n"
            )
            log_textbox.insert(ctk.END, texto_log)
            estado.set("✅ Descarga completada.")
            info["calidad"] = calidad  # añadimos calidad manualmente
            guardar_en_historial(info)  # guardamos en el historial

        except Exception as e:
            estado.set("❌ Error.")
            log_textbox.insert(ctk.END, f"❌ Error: {str(e)}")
            

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            carpeta_destino.set(carpeta)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    global ventana
    ventana = ctk.CTk()
    ventana.title("YouTube MP3 Downloader")
    ventana.geometry("600x500")
    ventana.resizable(False, False)

    entrada_url = ctk.StringVar()
    carpeta_destino = ctk.StringVar()
    calidad_var = ctk.StringVar(value="192")
    estado = ctk.StringVar(value="")
    progreso = ctk.DoubleVar(value=0)

    ctk.CTkLabel(ventana, text="🎵 Enlace del video de YouTube:", anchor="w").pack(pady=(20, 5), padx=20, anchor="w")
    ctk.CTkEntry(ventana, textvariable=entrada_url, width=500).pack(padx=20)

    ctk.CTkLabel(ventana, text="📁 Carpeta de destino:", anchor="w").pack(pady=(15, 5), padx=20, anchor="w")
    frame_carpeta = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_carpeta.pack(padx=20, fill="x")
    ctk.CTkEntry(frame_carpeta, textvariable=carpeta_destino, width=400).pack(side="left", padx=(0, 10))
    ctk.CTkButton(frame_carpeta, text="Seleccionar", command=seleccionar_carpeta, width=100).pack(side="left")

    ctk.CTkLabel(ventana, text="🎚️ Calidad MP3:", anchor="w").pack(pady=(15, 5), padx=20, anchor="w")
    ctk.CTkOptionMenu(ventana, variable=calidad_var, values=["128", "192", "320"]).pack(padx=20)

    ctk.CTkButton(ventana, text="Descargar MP3", command=descargar, fg_color="#4CAF50", width=200).pack(pady=25)

    ctk.CTkProgressBar(ventana, variable=progreso, width=400).pack(pady=5)
    ctk.CTkLabel(ventana, textvariable=estado, text_color="gray").pack(pady=5)

    global log_textbox
    log_textbox = ctk.CTkTextbox(ventana, width=540, height=100, corner_radius=8)
    log_textbox.pack(pady=10, padx=20)

    ventana.mainloop()
