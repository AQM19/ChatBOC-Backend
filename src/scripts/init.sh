# Creación del entorno virtual y su gestión. Hay que cambiar el intérprete del vscode a dicho entorno.
echo '**************************************************************************************************'
echo Creando entorno virtual
echo '**************************************************************************************************'

python3 -m venv .venv
source .venv/bin/activate
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
gnome-terminal -- sudo docker compose up

# Inicio de la api
echo '**************************************************************************************************'
echo Iniciando la aplicacion
echo '**************************************************************************************************'
python3 ./main.py