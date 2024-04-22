FROM debian:bullseye-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get remove -y python3-pip && apt-get autoremove -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia el resto de los archivos al directorio de trabajo
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Ejecuta la aplicación Flask cuando se inicie el contenedor
CMD ["python3", "app.py"]# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
FROM debian:bullseye-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get remove -y python3-pip && apt-get autoremove -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia el resto de los archivos al directorio de trabajo
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Ejecuta la aplicación Flask cuando se inicie el contenedor
CMD ["python3", "app.py"]
