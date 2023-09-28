# Procesador de Direcciones

Este script permite procesar y enriquecer un conjunto de datos con direcciones en Argentina. El objetivo es normalizar y geolocalizar estas direcciones utilizando distintas APIs.

## Funcionalidades

- Cargar datos desde un archivo CSV.
- Preprocesar los datos para normalizar los nombres de las columnas y los valores de las direcciones.
- Utilizar la API de Georef para normalizar y geolocalizar direcciones fuera de la Ciudad Autónoma de Buenos Aires (CABA).
- Utilizar las APIs de USIG para normalizar, geolocalizar y obtener información adicional (como barrio y comuna) para direcciones dentro de CABA.
- Combinar los resultados con el conjunto de datos original y visualizarlo.

## Archivo de entrada

El archivo de entrada debe ser un CSV con las siguientes columnas:

- `direccion`: La dirección que quieres normalizar y geolocalizar.
- `provincia`: La provincia donde se encuentra la dirección.
- `departamento`: El departamento o partido donde se encuentra la dirección.

Ejemplo de contenido del archivo CSV:

```python
direccion,provincia,departamento
Av. Santa Fe 1000,Ciudad Autónoma de Buenos Aires,
Roca 123,Buenos Aires,Quilmes
```


## Cómo usarlo

1) Asegúrate de tener Python instalado y configurado en tu máquina.
2) Clona este repositorio:

```python
git clone [URL_DEL_REPOSITORIO]
```

3) Instala las dependencias necesarias:
```python
pip install pandas requests
```

4) Ejecuta el script:
```python
python python [NOMBRE_DEL_ARCHIVO].py
```

## Dependencias

- `pandas`: Biblioteca para manipulación y análisis de datos.
- `requests`: Biblioteca para realizar peticiones HTTP.


## APIs utilizadas

- [Georef](https://apis.datos.gob.ar/georef/api.html): API del Gobierno de Argentina para normalizar y geolocalizar direcciones.
- [USIG](http://ws.usig.buenosaires.gob.ar/): Conjunto de APIs de la Ciudad Autónoma de Buenos Aires para procesar direcciones en CABA.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes alguna sugerencia, por favor abre un issue o realiza un pull request. Los cafecitos también:

[![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_1.svg)](https://cafecito.app/nievejuan21)
