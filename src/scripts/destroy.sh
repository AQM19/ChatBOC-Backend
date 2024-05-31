#!/bin/bash

# Detener y eliminar contenedores y volúmenes de Docker
echo '**************************************************************************************************'
echo Deteniendo y eliminando contenedores y volúmenes de Docker
echo '**************************************************************************************************'
docker compose down -v

docker stop ollama
docker rm ollama

# Eliminar archivos y directorios
echo '**************************************************************************************************'
echo Eliminando archivos y directorios
echo '**************************************************************************************************'

sudo rm -rf ./postgres/
sudo rm -rf ./chromadb/
rm -rf ./.venv
rm -rf ./.env

echo '**************************************************************************************************'
echo Operación completada
echo '**************************************************************************************************'
