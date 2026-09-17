# Social Media Analytics Dashboard

Aplicación Streamlit para analizar exportaciones CSV de Meta Business Suite de **Elebar** y **Punto Blu**. Ambos dashboards comparten la misma capa de ingestión, normalización, métricas, comparaciones, análisis y visualización, pero mantienen datasets independientes.

## Qué hace

- Importa uno o varios CSV.
- Identifica la marca por nombre/contenido; permite forzarla cuando sea necesario.
- Valida columnas y fechas y muestra errores/advertencias.
- Normaliza nombres de formatos y plataformas.
- Conserva valores ausentes como NA, no como cero.
- Integra períodos y evita duplicados mediante ID o clave estable.
- Calcula alcance, impresiones, frecuencia, interacciones, ER, video y crecimiento disponible.
- Compara el período seleccionado con el período anterior equivalente.
- Analiza publicaciones, formatos y días.
- Genera insights descriptivos sin afirmar causalidad.
- Permite exportar dataset, publicaciones y KPIs en CSV.

## Estructura

```text
app.py
dashboards/
  common.py
  elebar.py
  blu.py
src/
  data_loader.py
  data_validator.py
  data_cleaner.py
  repository.py
  ingestion.py
  metrics.py
  comparisons.py
  content_analysis.py
  charts.py
  insights.py
  utils.py
config/
  config.py
data/raw/{elebar,blu}/
data/processed/{elebar,blu}/tests/
assets/{elebar,blu}/
.streamlit/config.toml
requirements.txt
README.md
DATA_AUDIT.md
DATA_DICTIONARY.md
```

La arquitectura separa ingestión, validación, limpieza, persistencia, métricas, análisis y UI. La persistencia actual usa Parquet/CSV local, dejando `repository.py` como punto de reemplazo para una futura base de datos.

## Ejecutar localmente

Requiere Python 3.11+ recomendado.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Cargar CSV reales

Desde la barra lateral, abrir **Actualizar datos**, seleccionar uno o varios CSV y procesarlos. Los archivos no se modifican. Los datos normalizados quedan en `data/processed/elebar/` o `data/processed/blu/`.

También pueden conservarse los CSV originales en `data/raw/elebar/` y `data/raw/blu/`. Por privacidad y tamaño, esos archivos están ignorados por Git mediante `.gitignore`.

## Agregar una nueva marca

1. Agregar su configuración visual en `config/config.py`.
2. Crear su carpeta bajo `data/raw/` y `data/processed/`.
3. Incorporarla al selector de `app.py`.
4. Si requiere reglas específicas de Meta, ampliar `COLUMN_ALIASES`, `FORMAT_MAP` o la lógica de normalización.
5. Crear el wrapper en `dashboards/` reutilizando `render_dashboard`.

## Tipografía

La interfaz solicita `Museo Sans Rounded` y usa fuentes de respaldo si esa familia no está instalada en el equipo/servidor. No se incluye una fuente comercial en el repositorio.

## Tests

```bash
pytest -q
```

## GitHub + Streamlit Community Cloud

1. Crear un repositorio GitHub y subir el proyecto, sin CSV reales ni secretos.
2. En Streamlit Community Cloud, crear una app apuntando al repositorio y a `app.py`.
3. Configurar el entorno a partir de `requirements.txt`.
4. La URL resultante puede compartirse con múltiples usuarios.

Importante: la versión local usa archivos locales como persistencia. En Streamlit Community Cloud, el filesystem de la app no debe considerarse un almacén persistente para un flujo multiusuario. Para una versión publicada donde múltiples usuarios puedan cargar datos y esos datos deban sobrevivir reinicios/deploys, la siguiente evolución debe reemplazar `repository.py` por una base de datos o almacenamiento persistente. La UI y la lógica analítica pueden mantenerse.

## Seguridad y privacidad

No subir credenciales, tokens, secretos ni exportaciones reales de Meta al repositorio público. Si los datos contienen información sensible, usar un repositorio privado y revisar la política de acceso antes de publicar.

## Auditoría inicial de las carpetas de Windows

Para inventariar las exportaciones reales antes de incorporarlas al proyecto:

```bash
python scripts/audit_local_data.py
```

El script usa las rutas iniciales `C:\Users\alappano\Desktop\ELEBAR` y `C:\Users\alappano\Desktop\BLU`, no modifica los originales y genera `DATA_AUDIT_INVENTORY.csv` en la raíz del proyecto. Ese inventario no debe subirse si contiene información que no corresponda al repositorio.
