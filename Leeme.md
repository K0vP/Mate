# Documentación del Proyecto

## Estructura de Carpetas

- **assets**: Contiene las imágenes en caso de usar HTML.
- **frontend**: para la pagina si es el caso
    - **html**: para el orden de la pagina
    - **css**: para el diseño de la pagina
- **src**: Contiene el "backend" del proyecto.
  - **auth**: Autenticación de usuario o "iniciar sesión".
  - **models**: Clases y modelos de datos.
  - **export**: Funciones para exportar archivos (CSV, PDF, etc.).
  - **service**: Lógica de negocio (validaciones, asignaciones, etc.).
  - **config**: Constantes y configuraciones generales.
  - **database**: Todo lo relacionado con la base de datos.
  - **visualizar**: Contiene los gráficos y visualizaciones.

## Instrucciones

1. Asegúrate de tener instalado Python y las librerías necesarias.
2. Ejecuta `subir_excel.py` para seleccionar un archivo Excel.
3. Usa los scripts en la carpeta `src` para manejar la lógica del backend.