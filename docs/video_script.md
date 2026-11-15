# Guion de demostración — máximo 5 minutos

**Duración objetivo:** 4:30–4:50. Graba la pantalla y narra con voz clara. Usa únicamente URLs y resultados reales.

| Tiempo | Qué mostrar | Narración sugerida |
|---|---|---|
| 0:00–0:25 | Portada del repositorio GitHub | “Presento Sales Data Pipeline, un proyecto académico de Ingeniería de Datos que automatiza el procesamiento de datos de ventas con Python, PostgreSQL, GitHub Actions y Streamlit.” |
| 0:25–0:55 | Estructura del repositorio y CSV | “La fuente es un CSV sintético de demostración. El repositorio contiene el código ETL, pruebas, dashboard y workflow de automatización.” |
| 0:55–1:45 | `etl.py` y `main.py` | “La etapa Extract lee el CSV y valida sus columnas. Transform convierte tipos, trata valores faltantes, elimina duplicados y registros inválidos, y calcula el ingreso neto. Load almacena los datos en PostgreSQL usando `sale_id` para evitar duplicados en ejecuciones repetidas.” |
| 1:45–2:25 | PostgreSQL/Neon, tabla `sales` | “Los registros procesados se almacenan en PostgreSQL. La conexión se gestiona mediante una variable de entorno y no se incluyen credenciales en el repositorio.” |
| 2:25–3:10 | GitHub Actions, ejecución exitosa | “GitHub Actions instala dependencias, ejecuta pruebas y luego corre el ETL. El flujo puede iniciarse manualmente y también tiene una programación diaria.” |
| 3:10–4:20 | Dashboard Streamlit público | “El dashboard consulta PostgreSQL y muestra ingresos, cantidad de ventas, unidades, ticket promedio, evolución mensual, ingresos por categoría y productos más vendidos. Los filtros permiten explorar distintos periodos y categorías.” |
| 4:20–4:45 | README y enlaces | “El proyecto integra extracción, transformación, carga, automatización y visualización en una arquitectura sencilla y reproducible. En el repositorio se encuentran las instrucciones y evidencias.” |

## Antes de grabar

- [ ] Repositorio público y con README actualizado.
- [ ] GitHub Actions ejecutado correctamente.
- [ ] Base PostgreSQL con registros cargados.
- [ ] Dashboard público funcionando.
- [ ] Ocultar cualquier contraseña, token o secreto durante la grabación.
- [ ] Reemplazar la narración genérica por resultados reales donde corresponda.
- [ ] Duración final menor o igual a 5 minutos.
- [ ] Publicar el video como público o no listado, según acepte la consigna, y copiar su URL.

**Consejo:** evita grabar pantallas de configuración donde aparezcan credenciales. Puedes mostrar el nombre `DATABASE_URL`, pero nunca su valor.
