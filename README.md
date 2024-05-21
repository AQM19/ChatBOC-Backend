# ChatBOC

## Uso
Para la inicialización del proyecto se deberán seguir los siguientes pasos:

- Desactivar conda (si está previamente activado)
``` bash
conda deactivate
```
- Activar el entorno virtual local
``` bash
source chatboc-env/bin/activate
```
- Inicializar el docker de ollama
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
- Si no se tiene descargado el modelo se ha de ejecutar el siguiente comando para obtenerlo:
```bash
docker exec -it ollama ollama run llama3
```

## Colaboradores
-  Aarón Quintanal Martín
-  Daniel Villegas Celaya
-  Adrián Román González
-  Jesús Bueno González
-  Adolfo Sánchez López