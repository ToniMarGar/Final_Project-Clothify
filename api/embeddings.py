import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from database import get_db_connection

# Cargar el modelo preentrenado VGG16 para obtener embeddings de las imágenes
model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

def image_to_embedding(image: Image.Image):
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    
    embeddings = model.predict(image_array)
    embeddings = embeddings.flatten()
    return embeddings

def compare_embeddings(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def get_embeddings_from_db():
    # Conectarse a la base de datos y obtener las imágenes guardadas
    
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = "SELECT `Product ID`, `Image URLs` FROM `productos`"  # Cambia la tabla según tu estructura
    cursor.execute(query)
    
    results = cursor.fetchall()
    image_data = []
    
    for row in results:
        product_id = row[0]
        image_urls = row[1].split(',')  # Suponiendo que las URLs están separadas por comas
        
        for url in image_urls:
            image_data.append((product_id, url.strip()))  # Guardamos el ID y la URL de la imagen
    
    cursor.close()
    connection.close()
    
    return image_data