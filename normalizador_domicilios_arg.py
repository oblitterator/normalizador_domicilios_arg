import pandas as pd
import requests
from io import StringIO

def fetch_data(url=None, local_path=None):
    """Obtiene datos de una URL de GitHub o de una ruta local y devuelve un DataFrame."""
    
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            csv_data = response.text
            return pd.read_csv(StringIO(csv_data))
        else:
            raise ValueError(f"No se pudo obtener los datos. Código de estado: {response.status_code}")
    elif local_path:
        # Descomenta la línea de abajo si necesitas leer datos desde el entorno local.
        # return pd.read_csv(local_path)
        pass

def preprocess_dataframe(df):
    """Preprocesa el DataFrame para reemplazar valores y renombrar columnas."""
    # Reemplaza 'Capital' por 'Ciudad Autónoma de Buenos Aires'
    df = df.replace({'Capital': 'Ciudad Autónoma de Buenos Aires'})
    df.rename({'ciudad': 'departamento'}, axis=1, inplace=True)
    return df

def get_caba_additional_data(x, y):
    """Obtiene datos adicionales para CABA en función de las coordenadas x e y."""
    BASE_URL = 'http://ws.usig.buenosaires.gob.ar/datos_utiles'
    params = {'x': x, 'y': y}

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {'barrio': data.get('barrio', 'N/A'), 'comuna': data.get('comuna', 'N/A')}
    else:
        return {'barrio': 'N/A', 'comuna': 'N/A'}

def get_normalized_address(direccion, provincia, departamento=None):
    """Normalize an address using Georef API."""
    url_georef = "https://apis.datos.gob.ar/georef/api/direcciones"
    params = {
        "direccion": direccion,
        "provincia": provincia,
        "max": 5
    }
    if departamento:
        params["departamento"] = departamento

    response = requests.get(url_georef, params=params)
    if response.status_code == 200:
        return response.json().get("direcciones", None)
    else:
        return None

def normalize_and_geocode_address(calle, altura):
    """Normalize and geocode a CABA address using USIG API."""
    BASE_URL = 'http://ws.usig.buenosaires.gob.ar/rest'
    endpoint = '/normalizar_y_geocodificar_direcciones'
    params = {
        'calle': calle,
        'altura': altura,
        'desambiguar': 1
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def convert_coordinates(x, y):
    """Convert coordinates using USIG API."""
    BASE_URL = 'http://ws.usig.buenosaires.gob.ar/rest'
    endpoint = '/convertir_coordenadas'
    params = {
        'x': x,
        'y': y,
        'output': 'lonlat'
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json().get('resultado', None)
    else:
        return None

def main():
    COLUMNAS_REQUERIDAS = ["direccion", "provincia", "departamento"]
    
    # Paso 1: Cargar datos
    github_csv_url = "https://gist.githubusercontent.com/mgaitan/9677204/raw/1142ae2543fc819137b7e38370ee306208867a07/carrefour.csv"
    datos = fetch_data(url=github_csv_url)
    
    # Paso 2: Preprocesar datos
    datos = preprocess_dataframe(datos)
    # Verificar si las columnas requeridas están presentes
    columnas_faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in datos.columns]
    if columnas_faltantes:
        print(f"Error: Las columnas {', '.join(columnas_faltantes)} son necesarias para el procesamiento y no se encontraron en el archivo de entrada.")
        return
    
    # Paso 3: Procesar y enriquecer datos
    resultados = []
    for index, fila in datos.iterrows():
        partes = fila["direccion"].rsplit(' ', 1)
        calle = partes[0] if len(partes) > 1 else fila["direccion"]
        altura = partes[1] if len(partes) > 1 else "N/A"

        if fila["provincia"] == "Ciudad Autónoma de Buenos Aires":
            resultado_caba = normalize_and_geocode_address(calle, altura)
            if resultado_caba and 'GeoCodificacion' in resultado_caba:
                coordenadas_convertidas = convert_coordinates(resultado_caba['GeoCodificacion']['x'], resultado_caba['GeoCodificacion']['y'])
                datos_utiles = get_caba_additional_data(coordenadas_convertidas['x'], coordenadas_convertidas['y'])
                resultado = {
                    "Altura": altura,
                    "Calle": calle,
                    "Latitud": coordenadas_convertidas['y'],
                    "Longitud": coordenadas_convertidas['x'],
                    "Barrio": datos_utiles.get("barrio", "N/A"),
                    "Comuna": datos_utiles.get("comuna", "N/A")
                }
                resultados.append(resultado)
            else:
                resultados.append({
                    "Altura": altura,
                    "Calle": calle,
                    "Latitud": "N/A",
                    "Longitud": "N/A",
                    "Barrio": "N/A",
                    "Comuna": "N/A"
                })

        else:
            direcciones_normalizadas = get_normalized_address(fila["direccion"], fila["provincia"], fila["departamento"])
            if direcciones_normalizadas:
                direccion = direcciones_normalizadas[0]
                resultados.append({
                    "Altura": direccion["altura"]["valor"] if direccion["altura"] else "N/A",
                    "Calle": direccion["calle"]["nombre"] if direccion["calle"] else "N/A",
                    "Latitud": direccion["ubicacion"]["lat"] if direccion["ubicacion"] else "N/A",
                    "Longitud": direccion["ubicacion"]["lon"] if direccion["ubicacion"] else "N/A",
                    "Barrio": "N/A",
                    "Comuna": "N/A"
                })
            else:
                resultados.append({
                    "Altura": altura,
                    "Calle": calle,
                    "Latitud": "N/A",
                    "Longitud": "N/A",
                    "Barrio": "N/A",
                    "Comuna": "N/A"
                })

    # Paso 4: Combinar los resultados con los datos originales
    df_resultados = pd.DataFrame(resultados)
    for columna in df_resultados.columns:
        datos[columna] = df_resultados[columna]

    print(datos.head())

if __name__ == '__main__':
    main()
