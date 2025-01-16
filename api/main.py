from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
import numpy as np
from embeddings import image_to_embedding, compare_embeddings, get_embeddings_from_db

app = FastAPI()

@app.post("/compare_image/")
async def compare_image(file: UploadFile = File(...)):
    # Abrir la imagen recibida en la solicitud
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))

    # Obtener el embedding de la imagen recibida
    image_embedding = image_to_embedding(image)
    
    # Obtener las imágenes y embeddings almacenados en la base de datos
    image_data = get_embeddings_from_db()
    
    # Comparar la imagen recibida con las imágenes de la base de datos
    similarities = []
    
    for product_id, image_url in image_data:
        # Descargar la imagen desde la URL (simulado aquí por abrir la imagen)
        # Si las imágenes están almacenadas en un servidor, puedes descargarlas usando requests o urllib
        db_image = Image.open(BytesIO(image_bytes))  # Aquí debes descargar la imagen real
        
        # Obtener el embedding de la imagen de la base de datos
        db_image_embedding = image_to_embedding(db_image)
        
        # Comparar los embeddings
        similarity = compare_embeddings(image_embedding, db_image_embedding)
        similarities.append((product_id, similarity))
    
    # Ordenar por similitud descendente
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Retornar los 5 productos más similares
    top_5_similar = similarities[:5]
    
    return {"top_similar_products": top_5_similar}
