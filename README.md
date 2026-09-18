# Dashboard RRSS — Elebar / Punto Blu

Versión reconstruida desde cero para los CSV reales de Meta Business Suite compartidos durante el desarrollo.

- No contiene datos reales.
- No usa PyArrow ni Parquet.
- No requiere una columna `platform`: la plataforma se infiere de `FB-` / `IG-` y también puede inferirse de los datos.
- La fecha se obtiene de `Hora de publicación`; `Fecha` puede contener `Total` en estos exports.
- `Visualizaciones` no se convierte en impresiones.
- `Impresiones del anuncio` no se mezcla con impresiones orgánicas.
- Los datos cargados se mantienen en la sesión de Streamlit y pueden exportarse. Streamlit Cloud no es almacenamiento permanente.
