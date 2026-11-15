# Construcción de un Pipeline de Datos de Ventas con Python, PostgreSQL y GitHub Actions

> **Nota para publicación:** este artículo describe la implementación propuesta. Antes de publicarlo, completa los marcadores con evidencias obtenidas durante la ejecución. No afirmes que el despliegue o las pruebas fueron exitosos hasta verificarlos.

## Introducción

La Ingeniería de Datos permite convertir datos dispersos en información estructurada, confiable y disponible para el análisis. En contextos comerciales, los registros de ventas suelen almacenarse en archivos CSV y requieren tareas de limpieza, validación, integración y actualización antes de ser utilizados en reportes.

Este proyecto desarrolla **Sales Data Pipeline**, una solución académica que procesa un archivo CSV de ventas, transforma los registros con Python y Pandas, los almacena en PostgreSQL y presenta indicadores mediante un dashboard interactivo en Streamlit. La ejecución del proceso ETL se automatiza con GitHub Actions.

## Problema identificado

El uso directo de archivos CSV para elaborar reportes puede generar dificultades: registros duplicados, valores faltantes, formatos inconsistentes y cálculos manuales. Además, cuando la actualización depende de una persona, los indicadores pueden quedar desactualizados.

Se plantea un flujo reproducible que aplique reglas de calidad de datos y centralice la información procesada en una base de datos relacional.

## Objetivos

**Objetivo general:** implementar un pipeline automatizado para procesar, almacenar y visualizar datos demostrativos de ventas mediante herramientas accesibles de Ingeniería de Datos.

**Objetivos específicos:**
- Extraer registros comerciales desde un archivo CSV.
- Limpiar y transformar los datos mediante Pandas.
- Calcular ingresos considerando cantidad, precio y descuento.
- Cargar los registros procesados en PostgreSQL.
- Automatizar la ejecución ETL con GitHub Actions.
- Desarrollar y publicar un dashboard con Streamlit.

## Tecnologías utilizadas

- **Python:** lenguaje principal del proceso.
- **Pandas:** limpieza, tipado, deduplicación y enriquecimiento.
- **CSV:** fuente de datos demostrativa.
- **PostgreSQL:** almacenamiento relacional.
- **SQLAlchemy y psycopg2:** conexión y operaciones con PostgreSQL.
- **GitHub:** control de versiones y repositorio del código.
- **GitHub Actions:** automatización del pipeline.
- **Streamlit:** interfaz de visualización.
- **Streamlit Community Cloud:** alojamiento del dashboard.

## Arquitectura de la solución

El flujo comienza con `data/sales_demo.csv`. El módulo de extracción lee el archivo y verifica sus columnas. La transformación convierte tipos, elimina registros inválidos y duplicados, completa valores opcionales y calcula el ingreso neto. Finalmente, la carga crea la tabla `sales` si no existe y realiza inserciones o actualizaciones en función de `sale_id`.

GitHub Actions ejecuta las pruebas y el proceso ETL. Streamlit consulta PostgreSQL para presentar indicadores y gráficos.

**Diagrama:** [Insertar aquí el diagrama de arquitectura del README o una captura propia].

## Desarrollo del proceso ETL

### Extract

La función `extract()` lee el CSV con Pandas y verifica que existan las columnas obligatorias: identificador, fecha, producto, categoría, cantidad, precio unitario y tasa de descuento. Si faltan columnas, detiene el proceso para evitar una carga incorrecta.

### Transform

La función `transform()` aplica reglas de calidad:
- Convierte fechas y valores numéricos.
- Descarta filas sin identificador, fecha, producto, cantidad o precio válidos.
- Excluye cantidades no positivas y precios negativos.
- Completa la categoría faltante con “Sin categoría”.
- Sustituye descuentos faltantes por cero y limita la tasa al intervalo de 0 a 1.
- Elimina duplicados usando `sale_id`.

El ingreso se calcula mediante:

`revenue = quantity × unit_price × (1 − discount_rate)`

### Load

La función `load_to_postgres()` crea la tabla `sales` e inserta los registros. La clave primaria `sale_id` permite realizar una operación *upsert*: si el identificador ya existe, se actualizan sus atributos en lugar de generar otra fila. Esto hace que la ejecución repetida sea idempotente respecto a los identificadores procesados.

**Evidencia por agregar:** [captura de la tabla `sales` en PostgreSQL con datos cargados].

## Automatización con GitHub Actions

El workflow `.github/workflows/etl.yml` configura Python, instala las dependencias, ejecuta las pruebas automatizadas y después inicia el ETL. Puede activarse manualmente, mediante cambios relevantes en el repositorio o con una programación diaria.

La credencial de PostgreSQL se almacena como secreto del repositorio con el nombre `DATABASE_URL`. De esta forma, no es necesario escribir contraseñas en el código fuente.

**Evidencia por agregar:** [enlace o captura de una ejecución exitosa de GitHub Actions].

## Almacenamiento en PostgreSQL

PostgreSQL centraliza los datos depurados en la tabla `sales`. Se almacenan el identificador, fecha, producto, categoría, cantidad, precio, descuento e ingreso calculado. También se crean índices para facilitar consultas por fecha y categoría.

Para el despliegue se puede utilizar un servicio PostgreSQL administrado, por ejemplo Neon. La cadena de conexión se configura mediante variables de entorno y secretos.

## Despliegue del dashboard

La aplicación `app.py` utiliza Streamlit para consultar PostgreSQL y presentar:
- Ingresos totales.
- Cantidad de ventas y unidades vendidas.
- Ticket promedio.
- Ingresos por mes.
- Ingresos por categoría.
- Productos con mayor cantidad vendida.
- Filtros por periodo, categoría y producto.

El dashboard se publica en Streamlit Community Cloud conectado al repositorio de GitHub. La variable `DATABASE_URL` se configura en los secretos de la aplicación.

**Evidencia por agregar:** [captura del dashboard desplegado y URL pública].

## Resultados obtenidos

Completar esta sección después de ejecutar el proyecto. Registrar los resultados reales, por ejemplo:

- Filas leídas desde el CSV: **[NÚMERO REAL]**.
- Filas válidas después de la transformación: **[NÚMERO REAL]**.
- Filas insertadas o actualizadas en PostgreSQL: **[NÚMERO REAL]**.
- Pruebas automatizadas: **[RESULTADO REAL]**.
- Ejecución de GitHub Actions: **[URL REAL]**.
- Dashboard publicado: **[URL REAL]**.

No completar estos campos con valores estimados ni presentar datos sintéticos como ventas reales.

## Conclusiones

Sales Data Pipeline demuestra cómo integrar herramientas accesibles para construir un flujo ETL reproducible. Python y Pandas permiten aplicar reglas explícitas de calidad; PostgreSQL ofrece almacenamiento estructurado; GitHub Actions automatiza la ejecución y Streamlit facilita la exploración de indicadores.

Como mejora futura, el proyecto podría incorporar una fuente de datos transaccional, cargas incrementales, monitoreo, alertas y una herramienta de orquestación especializada. Para esta entrega académica se prioriza una arquitectura sencilla, verificable y de bajo costo, sin utilizar AWS.

## Enlaces del proyecto

- Repositorio: **[PEGAR URL PÚBLICA DE GITHUB]**
- Dashboard: **[PEGAR URL PÚBLICA DE STREAMLIT]**
- Video de demostración: **[PEGAR URL PÚBLICA DEL VIDEO]**
- Ejecución ETL: **[PEGAR URL DE GITHUB ACTIONS]**

---
**Autor:** [NOMBRE DEL ESTUDIANTE]  
**Curso:** [NOMBRE DEL CURSO]  
**Institución:** [NOMBRE DE LA UNIVERSIDAD]  
**Fecha:** [FECHA DE PUBLICACIÓN]
