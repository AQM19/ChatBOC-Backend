#!/bin/bash

# Función para detectar el sistema operativo
detect_os() {
    case "$OSTYPE" in
        linux*)   echo "Linux" ;;
        msys*)    echo "Windows" ;;
        cygwin*)  echo "Windows" ;;
        *)        echo "unknown" ;;
    esac
}

OS=$(detect_os)

# Creación del entorno virtual y su gestión
echo '**************************************************************************************************'
echo Creando entorno virtual
echo '**************************************************************************************************'

if [ "$OS" = "Linux" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
elif [ "$OS" = "Windows" ]; then
    python -m venv .venv
    .venv\Scripts\activate
else
    echo "Sistema operativo no soportado."
    exit 1
fi

pip install -r requirements.txt

# Copia del fichero de entornos
echo '**************************************************************************************************'
echo Copiando variables de entorno
echo '**************************************************************************************************'
cp .env.template .env

# Instancia de la base de los volúmenes y bases de datos
echo '**************************************************************************************************'
echo Creando instancia de ollama
echo '**************************************************************************************************'
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

if [ "$OS" = "Linux" ]; then
    gnome-terminal -- sudo docker compose up
elif [ "$OS" = "Windows" ]; then
    start cmd /c "docker compose up"
else
    echo "Sistema operativo no soportado."
    exit 1
fi

# Inicio de la api
echo '**************************************************************************************************'
echo Iniciando la aplicacion
echo '**************************************************************************************************'
if [ "$OS" = "Linux" ]; then
    python3 ./main.py
elif [ "$OS" = "Windows" ]; then
    python ./main.py
else
    echo "Sistema operativo no soportado."
    exit 1
fi

# # Creación del entorno virtual y su gestión. Hay que cambiar el intérprete del vscode a dicho entorno.
# echo '**************************************************************************************************'
# echo Creando entorno virtual
# echo '**************************************************************************************************'

# python3 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt

# # Copia del fichero de entornos
# echo '**************************************************************************************************'
# echo Copiando variables de entorno
# echo '**************************************************************************************************'
# cp .env.template .env

# # Instancia de la base de los volúmenes y bases de datos
# echo '**************************************************************************************************'
# echo Creando instancia de ollama
# echo '**************************************************************************************************'
# docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# gnome-terminal -- sudo docker compose up

# # Inicio de la api
# echo '**************************************************************************************************'
# echo Iniciando la aplicacion
# echo '**************************************************************************************************'
# python3 ./main.py