# ChatBOC

Aplicación de integración de la inteligencia artificial a un chatbot con el cual se puede preguntar sobre cualquier cosa sobre el BOC (Boletín Oficial de Cantabria).

## Uso
Para la inicialización del proyecto se deberán seguir los siguientes pasos:

- Borrar la carpeta `./postgres`
- Borrar el volumen de base de datos:
    ```bash
    docker compose down -v
    ```
- Parar el servicio docker de ollama
    ```bash
    docker stop ollama
    ```
- Borrar servicio docker de ollama
    ```bash
    docker rm ollama
    ```
- Ejecutar el script de inicio rápido (en windows inicializar con `WSL` o `GitBash`):
    ```bash
    .\init.sh
    ```

## Preparación del entorno
- Activar el entorno virtual local
    ``` bash
    source chatboc-env/bin/activate
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