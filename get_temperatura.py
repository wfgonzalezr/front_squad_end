import os
import requests
from google.cloud import storage
from flask import jsonify

def get_temperatura(request):
    # Coordenadas de Santiago, Chile
    latitude = -33.459229
    longitud = -70.645348

    # URL para obtener los datos de Open-Meteo
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitud}&hourly=temperature_2m"

    # Hacer la solicitud a la API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        horas = data['hourly']['time']
        temperaturas = data['hourly']['temperature_2m']

        # Crear el resultado como una lista de diccionarios
        resultado = [
            {'hora': hora, 'temperatura_celsius': temp}
            for hora, temp in zip(horas, temperaturas)
        ]
        
        # Nombre del bucket y archivo a guardar
        bucket_name = 'laboratorio_dataplex'  # Nombre de tu bucket
        file_name = 'temperaturas.csv'  # Nombre del archivo a crear
        
        # Crear el cliente de Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Convertir los datos a CSV y subir al bucket
        csv_data = 'hora,temperatura_celsius\n'
        for item in resultado:
            csv_data += f"{item['hora']},{item['temperatura_celsius']}\n"
        
        # Subir los datos al bucket
        blob.upload_from_string(csv_data, content_type='text/csv')

        # Responder con mensaje de éxito
        return jsonify({'message': 'Datos escritos correctamente en el bucket', 'data': resultado})
    
    else:
        return f"Error al obtener datos: {response.status_code}", 500
