# ChatBOC

Aplicación de integración de la inteligencia artificial a un chatbot con el cual se puede preguntar sobre cualquier cosa sobre el BOC (Boletín Oficial de Cantabria).

## Preparación del entorno

Para poder iniciar por primera vez la aplicación de manera correcta hacen falta dos pasos:

- Ejecutar el script de inicio alojado en la carpeta de scripts `src/scripts/init.sql`
    ```bash
    ./src/scripts/init.sql
    ```
    <p style="color:#5BC0de">Con hacerlo en Windows se va a tener que utilizar WSL o GitBash</p>

- Si no se tiene descargado el modelo se ha de ejecutar el siguiente comando para obtenerlo:
    ```bash
    docker exec -it ollama ollama run llama3
    ```
    <p style="color:#5BC0de">Si no se tiene el modelo de ollama de manera local, cuando se quiera hacer una petición al modelo se obtendrá un error alegando que no se puede generar instancia del modelo llama3</p>

## Eliminación completa del entorno

Con tal de hacer un `hard reset` en el proyecto, se ejecutará el script alojado en la carpeta de scripts `src/scripts/destroy.sh`, el cual se encargará de:

-   Eliminar el volumen de docker creado
-   Parar el servicio de `ollama` y eliminarlo
-   Eliminar la carpeta contenedora de la base de datos
-   Eliminar el entorno virtual `.venv`
-   Eliminar el archivo de variables de entorno `.evn`

## Colaboradores
<ul>
    <li style=color:#22bb33>Daniel Villegas Celaya (Gestor)</li>
    <li style=color:#5bc0de>Jesús Bueno González</li>
    <li style=color:#aaaaaa>Adolfo Sánchez López (Portavoz)</li>
    <li style=color:#bb2124>Aarón Quintanal Martín (Secretario)</li>
    <li style=color:#f0ad4e>Adrián Román González</li>
</ul>