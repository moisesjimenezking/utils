FROM python:3.9-alpine

# Copia los archivos necesarios al contenedor
COPY .env .env
COPY requirements.txt .

# Instala pip y las dependencias del proyecto
RUN python -m pip install --upgrade pip
RUN apk update && pip install -r requirements.txt
RUN apk update && apk add openssh-client sshpass curl

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia la aplicación al contenedor
COPY app /app

# Especifica el comando que se ejecutará cuando se inicie el contenedor
CMD ["python3", "run.py"]