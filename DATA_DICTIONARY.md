# Diccionario de datos normalizado

| Campo | Tipo | Descripción | Ausencia |
|---|---|---|---|
| date | date | Fecha de publicación | NA |
| time | string | Hora de publicación | NA |
| platform | string | Instagram/Facebook u otra red detectada | NA |
| account | string | Cuenta/página | NA |
| post_id | string | ID de publicación, si Meta lo entrega | NA |
| url | string | URL/permalink | NA |
| format | string | Post, Carrusel, Reel, Video o Imagen | NA |
| content_type | string | Tipo/categoría de contenido | NA |
| copy | string | Texto/copy disponible | NA |
| reach | number | Alcance | NA, no 0 |
| impressions | number | Impresiones | NA, no 0 |
| video_views | number | Reproducciones | NA, no 0 |
| likes | number | Me gusta/reacciones según exportación | NA, no 0 |
| comments | number | Comentarios | NA, no 0 |
| shares | number | Compartidos | NA, no 0 |
| saves | number | Guardados | NA, no 0 |
| clicks | number | Clics | NA, no 0 |
| profile_visits | number | Visitas al perfil | NA, no 0 |
| followers_gained | number | Seguidores ganados | NA, no 0 |
| followers_lost | number | Seguidores perdidos | NA, no 0 |
| interactions | number | Likes + comentarios + compartidos + guardados, si no existe en origen | NA |
| er_reach | number | Interacciones / alcance × 100 | NA |
| er_impressions | number | Interacciones / impresiones × 100 | NA |
| video_duration_seconds | number | Duración del video | NA |
| source_file | string | Archivo de origen | — |
| source_row | integer | Fila de origen | — |
| brand | string | ELEBAR / PUNTO BLU | — |

La regla general es no convertir una métrica ausente en cero. Cero se conserva cuando el archivo realmente informa cero.
