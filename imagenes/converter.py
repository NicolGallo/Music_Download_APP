from PIL import Image
import os

# Carpeta donde están las imágenes
carpeta_imagenes = 'imagenes'  # Cambia esto si tus imágenes están en otra carpeta

# Obtener todas las imágenes JPG o JPEG
imagenes = [f for f in os.listdir(carpeta_imagenes) if f.lower().endswith(('.jpg', '.jpeg'))]
imagenes.sort()  # Opcional: ordena por nombre

# Cargar imágenes
imagenes_pil = [Image.open(os.path.join(carpeta_imagenes, img)).convert('RGB') for img in imagenes]

# Guardar en un solo PDF
if imagenes_pil:
    imagenes_pil[0].save("salida.pdf", save_all=True, append_images=imagenes_pil[1:])
    print("PDF generado como 'salida.pdf'")
else:
    print("No se encontraron imágenes JPG/JPEG en la carpeta.")
