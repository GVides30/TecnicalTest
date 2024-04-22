import os
import requests
import json
from datetime import datetime
import csv
import re

# Ruta donde se encuentra el script
script_path = os.path.dirname(os.path.realpath(__file__))

# Extraer datos diarios de la API y guardarlos como archivo JSON
api_url = 'https://dummyjson.com/users'
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    current_date = datetime.now().strftime('%Y%m%d')
    file_name = os.path.join(script_path, f'data_{current_date}.json')
    with open(file_name, 'w') as f:
        json.dump(data, f)

    # Definir csv_file_name y summary_file_name antes de la verificación
    csv_file_name = os.path.join(script_path, f'ETL_{current_date}.csv')
    summary_file_name = os.path.join(script_path, f'summary_{current_date}.csv')

    # Transformar los datos del archivo JSON a un archivo CSV
    if isinstance(data, dict) and 'users' in data:  # Verificar si data es una lista no vacía
        with open(csv_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data['users'][0].keys())  # Escribir encabezados de columna
            for row in data['users']:
                csvwriter.writerow(row.values())
    else:
        print('Error: Los datos no están en el formato esperado.')

    # Total de registros
    total_registros = len(data['users'])

    # Cantidad de registros por género
    generos = {}
    for usuario in data['users']:
        genero = usuario['gender']
        if genero in generos:
            generos[genero] += 1
        else:
            generos[genero] = 1

    # Edades de cada género agrupadas
    edades = {'male': {}, 'female': {}, 'other': {}}
    for usuario in data['users']:
        genero = usuario['gender']
        edad = usuario['age']
        if edad <= 10:
            grupo_edad = '00-10'
        elif edad <= 20:
            grupo_edad = '11-20'
        elif edad <= 30:
            grupo_edad = '21-30'
        elif edad <= 40:
            grupo_edad = '31-40'
        elif edad <= 50:
            grupo_edad = '41-50'
        elif edad <= 60:
            grupo_edad = '51-60'
        elif edad <= 70:
            grupo_edad = '61-70'
        elif edad <= 80:
            grupo_edad = '71-80'
        elif edad <= 90:
            grupo_edad = '81-90'
        else:
            grupo_edad = '91+'

        if grupo_edad in edades[genero]:
            edades[genero][grupo_edad] += 1
        else:
            edades[genero][grupo_edad] = 1

    # Ciudades ocupadas, divididas por género y también por sistema operativo
    ciudades = {}
    for usuario in data['users']:
        ciudad = usuario['address']['city']
        so = usuario['userAgent'].split('(')[-1].split(' ')[0]
        genero = usuario['gender']
        if ciudad in ciudades:
            if so in ciudades[ciudad]:
                ciudades[ciudad][so][genero] = ciudades[ciudad][so].get(genero, 0) + 1
            else:
                ciudades[ciudad][so] = {genero: 1}
        else:
            ciudades[ciudad] = {so: {genero: 1}}

    # Definir patrones de expresiones regulares para los sistemas operativos
    windows_pattern = re.compile(r"Windows")
    apple_pattern = re.compile(r"Macintosh|iPad|iPhone|Mac OS X")
    linux_pattern = re.compile(r"Linux")

    # Contadores para los sistemas operativos
    windows_count = 0
    apple_count = 0
    linux_count = 0
    other_count = 0

    # Iterar sobre los datos para contar los sistemas operativos
    for user_data in data['users']:
        user_agent = user_data.get('userAgent', '')
        if windows_pattern.search(user_agent):
            windows_count += 1
        elif apple_pattern.search(user_agent):
            apple_count += 1
        elif linux_pattern.search(user_agent):
            linux_count += 1
        else:
            other_count += 1

    # Crear el summary.csv
    with open(summary_file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['registro', total_registros])
        csvwriter.writerow([])
        csvwriter.writerow(['gender', 'total'])
        for genero, cantidad in generos.items():
            csvwriter.writerow([genero, cantidad])
        csvwriter.writerow([])
        csvwriter.writerow(['age', 'male', 'female'])
        for grupo_edad in ['00-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91+']:
            csvwriter.writerow([grupo_edad, edades['male'].get(grupo_edad, 0), edades['female'].get(grupo_edad, 0)])
        csvwriter.writerow([])
        csvwriter.writerow(['City', 'male', 'female'])
        for ciudad, generos_ciudad in ciudades.items():
            for so, generos_so in generos_ciudad.items():
                male_count = generos_so.get('male', 0)
                female_count = generos_so.get('female', 0)
                csvwriter.writerow([ciudad, male_count, female_count])
        csvwriter.writerow([])
        summary_csvwriter = csv.writer(csvfile)
        summary_csvwriter.writerow(['SO', 'total'])
        summary_csvwriter.writerow(['Windows', windows_count])
        summary_csvwriter.writerow(['Apple', apple_count])
        summary_csvwriter.writerow(['Linux', linux_count])
        summary_csvwriter.writerow(['Other', other_count])
        print('Proceso completado. Archivos CSV generados:', csv_file_name, summary_file_name)
else:
    print('Error al obtener los datos de la API')
