import sqlite3
import pandas as pd
from datetime import datetime

current_date = datetime.now().strftime('%Y%m%d')

# Leer el archivo 'ETL_{current_date}.csv' y agregar la columna 'date_insertion'
detail_df = pd.read_csv(f'ETL_{current_date}.csv')
detail_df.insert(detail_df.columns.get_loc('id') + 1, 'date_insertion', pd.Timestamp.now())

# Guardar el DataFrame 'detail_df' en la tabla 'detail' de la base de datos
connection = sqlite3.connect('database/usuarios.db')
detail_df.to_sql('detail', connection, if_exists='replace', index=False)
connection.close()

# Leer el archivo 'summary_{current_date}.csv' y completar las líneas con valores nulos si no tienen 3 columnas
try:
    summary_df = pd.read_csv(f'summary_{current_date}.csv')
except pd.errors.ParserError:
    print(f"Error al leer el archivo 'summary_{current_date}.csv'. Se omitirán las líneas con errores.")
    with open(f'summary_{current_date}.csv', 'r') as file:
        lines = file.readlines()
    data = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 3:
            parts += [None] * (3 - len(parts))  # Completa con valores nulos si no hay 3 columnas
        data.append(parts)
    summary_df = pd.DataFrame(data, columns=['col1', 'col2', 'col3'])

summary_df.columns = summary_df.columns.str.strip()

# Agregar las columnas 'id' y 'date_insertion' a 'summary_df'
summary_df.insert(0, 'id', range(1, 1 + len(summary_df)))
summary_df.insert(1, 'date_insertion', pd.Timestamp.now())

# Guardar el DataFrame 'summary_df' en la tabla 'summary' de la base de datos
connection = sqlite3.connect('database/usuarios.db')
summary_df.to_sql('summary', connection, if_exists='replace', index=False)

# Obtener los IDs de los últimos registros insertados en 'summary' y 'detail'
cursor = connection.cursor()
cursor.execute("SELECT MAX(id) FROM summary")
summary_id = cursor.fetchone()[0]
cursor.execute("SELECT MAX(id) FROM detail")
detail_id = cursor.fetchone()[0]

# Crear la tabla 'process' si no existe
connection.execute('''
    CREATE TABLE IF NOT EXISTS process (
        id INTEGER PRIMARY KEY,
        summary_id INTEGER,
        detail_id INTEGER,
        execution_date DATE
    )
''')

# Insertar un nuevo registro en 'process' con los IDs obtenidos y la fecha de ejecución
connection.execute(f"INSERT INTO process (summary_id, detail_id, execution_date) VALUES ({summary_id}, {detail_id}, '{current_date}')")

connection.commit()
connection.close()
