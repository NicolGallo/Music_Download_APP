import customtkinter as ctk
from tkinter import filedialog
import threading  # 1. Importamos la librería de hilos
from core.downloader import descargar_mp3

def iniciar_gui():
    def progreso_hook(d):
        if d['status'] == 'downloading':
            porcentaje = d.get('_percent_str', '0.0%').strip().replace('%', '')
            try:
                # CustomTkinter permite actualizar variables desde hilos de forma segura
                progreso.set(float(porcentaje))
            except ValueError:
                progreso.set(0)
        elif d['status'] == 'finished':
            progreso.set(100)

    # 2. Esta es la función que hará el trabajo pesado en segundo plano
    def hilo_descarga(url, carpeta, calidad):
        try:
            estado.set("⏳ Descargando...")
            progreso.set(0)
            
            # Llamada a la función de descarga
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
            
            # Actualizamos la UI al terminar
            log_textbox.insert(ctk.END, texto_log)
            estado.set("✅ Descarga completada.")
            
            info["calidad"] = calidad

        except Exception as e:
            estado.set("❌ Error.")
            log_textbox.insert(ctk.END, f"❌ Error: {str(e)}")
        
        # Reactivamos el botón al finalizar
        boton_descarga.configure(state="normal")

    def iniciar_proceso_descarga():
        url = entrada_url.get().strip()
        carpeta = carpeta_destino.get().strip()
        calidad = calidad_var.get()
        
        if not url or not carpeta:
            estado.set("❌ Faltan datos.")
            return

        log_textbox.delete("0.0", ctk.END)
        
        # Desactivamos el botón para evitar múltiples descargas simultáneas
        boton_descarga.configure(state="disabled")
        
        # 3. Creamos y lanzamos el hilo
        threading.Thread(target=hilo_descarga, args=(url, carpeta, calidad), daemon=True).start()

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            carpeta_destino.set(carpeta)

    # --- Configuración de la Ventana (Igual que antes) ---
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("YouTube MP3 Downloader")
    ventana.geometry("600x500")
    ventana.resizable(False, False)

    entrada_url = ctk.StringVar()
    carpeta_destino = ctk.StringVar()
    calidad_var = ctk.StringVar(value="192")
    estado = ctk.StringVar(value="")
    progreso = ctk.DoubleVar(value=0)

    # UI Elements
    ctk.CTkLabel(ventana, text="🎵 Enlace del video de YouTube:", anchor="w").pack(pady=(20, 5), padx=20, anchor="w")
    ctk.CTkEntry(ventana, textvariable=entrada_url, width=500).pack(padx=20)

    ctk.CTkLabel(ventana, text="📁 Carpeta de destino:", anchor="w").pack(pady=(15, 5), padx=20, anchor="w")
    frame_carpeta = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_carpeta.pack(padx=20, fill="x")
    ctk.CTkEntry(frame_carpeta, textvariable=carpeta_destino, width=400).pack(side="left", padx=(0, 10))
    ctk.CTkButton(frame_carpeta, text="Seleccionar", command=seleccionar_carpeta, width=100).pack(side="left")

    ctk.CTkLabel(ventana, text="🎚️ Calidad MP3:", anchor="w").pack(pady=(15, 5), padx=20, anchor="w")
    ctk.CTkOptionMenu(ventana, variable=calidad_var, values=["128", "192", "320"]).pack(padx=20)

    # Guardamos la referencia del botón para poder activarlo/desactivarlo
    boton_descarga = ctk.CTkButton(ventana, text="Descargar MP3", command=iniciar_proceso_descarga, fg_color="#4CAF50", width=200)
    boton_descarga.pack(pady=25)

    ctk.CTkProgressBar(ventana, variable=progreso, width=400).pack(pady=5)
    ctk.CTkLabel(ventana, textvariable=estado, text_color="gray").pack(pady=5)

    log_textbox = ctk.CTkTextbox(ventana, width=540, height=100, corner_radius=8)
    log_textbox.pack(pady=10, padx=20)

    ventana.mainloop()