# Auditoría de datos

Estado inicial: **pendiente de ejecutar sobre los CSV reales**.

Las carpetas locales indicadas para la primera auditoría son:

- `C:\Users\alappano\Desktop\ELEBAR`
- `C:\Users\alappano\Desktop\BLU`

Este entorno de ejecución no tiene acceso directo al Escritorio de Windows del usuario, por lo que no se inventaron resultados ni se copiaron datos ficticios al proyecto.

## Procedimiento previsto

1. Inventariar todos los CSV de ambas carpetas.
2. Registrar nombre, tamaño, fecha de modificación y período inferido.
3. Identificar columnas y variaciones entre exportaciones.
4. Validar fechas, tipos, nulos y duplicados.
5. Mapear columnas a `DATA_DICTIONARY.md`.
6. Copiar únicamente los archivos destinados al repositorio local bajo `data/raw/`; conservar originales sin modificar.

El sistema ya contiene la capa de normalización para tolerar diferencias razonables entre exportaciones. Una vez disponibles los CSV reales, conviene completar este documento con el inventario real antes de cerrar el mapeo definitivo.
