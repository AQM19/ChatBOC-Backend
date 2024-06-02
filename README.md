# ChatBOC

Aplicación de integración de la inteligencia artificial a un chatbot con el cual se puede preguntar sobre cualquier cosa sobre el BOC (Boletín Oficial de Cantabria).

# Bases de datos

Las bases de datos que utilizará el proyecto serán:

## PostgreSQL
Base de datos relacional donde se tendrán en cuenta los diferentes usuarios, roles y chats que se manejarán desde la página web.

## ChromaDB
Base de datos vectorial que almacenará todos los PDF que se obtengan del BOC. Será la proveedora del contexto para las preguntas que se le hagan al modelo de la inteligencia artificial.

# Entorno y despliegue

Los scripts que se nombra a continuación harán distinción del sistema operativo con el que se ejecuten.

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

# Uso

Para poder utilizar esta aplcación debe estar completamente desplegada, es decir, haber iniciado en el servidor, local o remoto, el script de inicio anteriormente mencionado.

Una vez desplegado, para poder hacer un correcto uso de la aplicación, se debe viajar a la ruta de la página web (previamente desplegada igualmente) y registrarse. Con el registro se podrá acceder al login de la aplicación, el cual retornará un token de autenticación que se extendá a lo largo del servidor con la sesión.

A la API es implosible acceder sin un token de autenticación ya que dispone de la verifiación jwt, lo cual hace que si no se manda por las cabeceras de la petición el token jwt de autenticación correspondiente no se podrá hacer uso de ello.

Una vez ingresado en la aplicacion, se debe crear un chat manualmente y comenzar a escribir en ello. El modelo dará una respuesta una vez haya procesado toda la información necesaria.

# Colaboradores
<ul>
    <li style=color:#22bb33>Daniel Villegas Celaya (Gestor)</li>
    <li style=color:#5bc0de>Jesús Bueno González</li>
    <li style=color:#aaaaaa>Adolfo Sánchez López (Portavoz)</li>
    <li style=color:#bb2124>Aarón Quintanal Martín (Secretario)</li>
    <li style=color:#f0ad4e>Adrián Román González</li>
</ul>