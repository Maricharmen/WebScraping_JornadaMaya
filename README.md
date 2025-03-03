# Web Scraping

Recuperación de información de la página web **La Jornada Maya** mediante técnicas de *web scraping*.

Presentacion [Link](https://www.canva.com/design/DAGgjol0fKg/XDfiXU9-gvmju_lxl_8qoQ/edit?utm_content=DAGgjol0fKg&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Información Recopilada
El scraping extrae los siguientes detalles de cada artículo:

- **Fecha**
- **Título**
- **Autor** (si está disponible).
- **Traductor** (si está disponible).
- **Ubicación** (si está disponible).
- **Contenido**

## Estructura

El archivo `.csv` generado se llama **`datos_analisis.csv`** y tiene la siguiente estructura:

| Fecha       | Autor        | Traductor     | Ubicacion     | Titulo       | Contenido      |
|-------------|--------------|---------------|---------------|--------------|----------------|
| 02/03/2025  | Juan Pérez   | Ana Gómez     | Cancún        | Ejemplo 1    | Texto del artículo 1... |
| 03/03/2025  | María López  | Desconocido   | Playa del Carmen | Ejemplo 2 | Texto del artículo 2...  |

### Funciones Principales

1. **`get_links(url)`**: Recupera todos los enlaces de artículos de una página específica (por mes)
   
2. **`find_all_links_in_month(month)`**: Construye la URL de la página correspondiente al mes y llama a `get_links()` para obtener los enlaces de artículos publicados en ese mes.

3. **`get_info(link)`**: Extrae la información de un artículo a partir de su enlace:
   - Título
   - Fecha
   - Autor
   - Traductor
   - Ubicación
   - Contenido

4. **`scraping()`**: Procesa el scraping para cada mes del año, recuperando los enlaces y los detalles de cada artículo, y guardándolos en un archivo `.csv` llamado `datos_analisis.csv`.

## Ejecución

```bash
python main.py
