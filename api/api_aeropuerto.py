from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Aeropuerto(BaseModel):
    name: str
    location: str
    code: str

@app.get("/aeropuertos/")
def get_aeropuertos():
    try:
        with open('api_aeropuerto.json', 'r', encoding='utf-8') as archivo:
            datos_dict = json.load(archivo)
        return {"mensaje": "data found", "data": datos_dict}
    except:
        return {"mensaje": "Data not found"}

@app.get("/aeropuertos/{item_id}")
def get_aeropuerto(item_id: int):
    with open('api_aeropuerto.json', 'r', encoding='utf-8') as archivo:
        datos_dict = json.load(archivo)
    try:
        return {"mensaje": "data found", "data": datos_dict[item_id]}
    except:
        return {"mensaje": "ID not found", "id": item_id}

@app.post("/aeropuertos/")
def create_aeropuerto(aeropuerto: Aeropuerto = None):
    try:
        new_data = aeropuerto.model_dump(mode='json')
        with open("api_aeropuerto.json", 'r', encoding='utf-8') as archivo:
            existing_data = json.load(archivo)

        existing_data.append(new_data)

        with open("api_aeropuerto.json", "w", encoding='utf-8') as archivo:
            json.dump(existing_data, archivo, indent=2)
        return {"mensaje": "Data inserted", "data": new_data}
    except:
        return {"mensaje": "Error, Data not inserted"}

@app.put("/aeropuertos/{item_id}")
def update_aeropuerto(item_id: int, aeropuerto: Aeropuerto = None):
    try:
        new_data = aeropuerto.model_dump(mode='json')
        with open("api_aeropuerto.json", 'r', encoding='utf-8') as archivo:
            existing_data = json.load(archivo)

        existing_data[item_id] = new_data

        with open("api_aeropuerto.json", "w", encoding='utf-8') as archivo:
            json.dump(existing_data, archivo, indent=2)
        return {"mensaje": "data updated", "data": new_data}
    except:
        return {"mensaje": "Error, data not updated"}

@app.delete("/aeropuertos/{item_id}")
def delete_aeropuerto(item_id: int):
    try:
        with open("api_aeropuerto.json", 'r', encoding='utf-8') as archivo:
            existing_data = json.load(archivo)

        copy_data = existing_data[item_id]
        existing_data.pop(item_id)
        
        with open("api_aeropuerto.json", "w", encoding='utf-8') as archivo:
            json.dump(existing_data, archivo, indent=2)
        return {"mensaje": "data deleted", "data": copy_data}
    except:
        return {"mensaje": "ID not found", "id": item_id}

class Ruta(BaseModel):
    distance: str
    flight_time: str
    airport_a: str
    airport_b: str

@app.get("/rutas/")
def get_rutas():
    try:
        with open('api_ruta.json', 'r', encoding='utf-8') as archivo:
            datos_dict = json.load(archivo)
        return {"mensaje": "data found", "data": datos_dict}
    except:
        return {"mensaje": "Data not found"}

@app.get("/rutas/{item_id}")
def get_ruta(item_id: int):
    with open('api_ruta.json', 'r', encoding='utf-8') as archivo:
        datos_dict = json.load(archivo)
    try:
        return {"mensaje": "data found", "data": datos_dict[item_id]}
    except:
        return {"mensaje": "ID not found", "id": item_id}

@app.post("/rutas/")
def create_ruta(ruta: Ruta = None):
    try:
        new_data = ruta.model_dump(mode='json')
        with open("api_ruta.json", 'r', encoding='utf-8') as archivo:
            existing_data = json.load(archivo)

        existing_data.append(new_data)

        with open("api_ruta.json", "w", encoding='utf-8') as archivo:
            json.dump(existing_data, archivo, indent=2)
        return {"mensaje": "Data inserted", "data": new_data}
    except:
        return {"mensaje": "Error, Data not inserted"}

@app.put("/rutas/{item_id}")
def update_ruta(item_id: int, ruta: Ruta = None):
    try:
        new_data = ruta.model_dump(mode='json')
        with open("api_ruta.json", 'r', encoding='utf-8') as archivo:
            existing_data = json.load(archivo)

        existing_data[item_id] = new_data

        with open("api_ruta.json", "w", encoding='utf-8') as archivo:
            json.dump(existing_data, archivo, indent=2)
        return {"mensaje": "data updated", "data": new_data}
    except:
        return {"mensaje": "Error, data not updated"}

@app.delete("/rutas/{item_id}")
def delete_ruta(item_id: int):
    try:
        with open("api_ruta.json", 'r', encoding='utf-8') as archivo:
            existing_data = json.load(archivo)

        copy_data = existing_data[item_id]
        existing_data.pop(item_id)
        
        with open("api_ruta.json", "w", encoding='utf-8') as archivo:
            json.dump(existing_data, archivo, indent=2)
        return {"mensaje": "data deleted", "data": copy_data}
    except:
        return {"mensaje": "ID not found", "id": item_id}