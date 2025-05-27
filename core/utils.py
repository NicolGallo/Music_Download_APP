import json
import os
from datetime import datetime

def guardar_en_historial(info):
    # Carpeta fija dentro del proyecto
    carpeta = os.path.join(os.getcwd(), "data")
    os.makedirs(carpeta, exist_ok=True)

    archivo = os.path.join(carpeta, "historial_descargas.json")

    entrada = {
        "titulo": info.get("titulo", "Desconocido"),
        "duracion": f"{info.get('duracion', 0) // 60}:{info.get('duracion', 0) % 60:02d}",
        "tamanio_mb": round(info.get("tamanio", 0) / 1024 / 1024, 2),
        "url": info.get("url"),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "calidad": info.get("calidad", "192")
    }

    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = []

    historial.append(entrada)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

    print(f"✅ Historial actualizado: {archivo}")
