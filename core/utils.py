import json
import os
from datetime import datetime

def guardar_en_historial(info):
    carpeta = os.path.join(os.getcwd(), "data")
    os.makedirs(carpeta, exist_ok=True)

    archivo = os.path.join(carpeta, "historial_descargas.json")

    nueva_url = info.get("url")

    # Leer historial si existe
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = []

    # Verificar si ya existe una entrada con la misma URL (independiente de la calidad)
    ya_descargado = any(entrada["url"] == nueva_url for entrada in historial)

    if ya_descargado:
        print(f"🔁 El video ya está en el historial. No se añade de nuevo.")
        return  # No guardar duplicado

    # Crear nueva entrada
    entrada = {
        "titulo": info.get("titulo", "Desconocido"),
        "duracion": f"{info.get('duracion', 0) // 60}:{info.get('duracion', 0) % 60:02d}",
        "tamanio_mb": round(info.get("tamanio", 0) / 1024 / 1024, 2),
        "url": nueva_url,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "calidad": info.get("calidad", "192")
    }

    historial.append(entrada)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

    print(f"✅ Entrada añadida al historial.")
