<<<<<<< HEAD
# Sales Data Pipeline
**Sistema automatizado de procesamiento y análisis de ventas**

Proyecto académico de Ingeniería de Datos que implementa un flujo ETL con Python y Pandas, persiste los datos en PostgreSQL, automatiza la ejecución mediante GitHub Actions y presenta indicadores con Streamlit.

> **Aviso:** `data/sales_demo.csv` contiene datos sintéticos creados exclusivamente para demostración académica. No corresponden a clientes ni transacciones reales.

## 1. Arquitectura

```mermaid
flowchart LR
    A[CSV de ventas] --> B[Extract: Pandas]
    B --> C[Transformación y validación]
    C --> D[Load: PostgreSQL]
    E[GitHub Actions] --> B
    D --> F[Streamlit Community Cloud]
    F --> G[Dashboard interactivo]
```

- **Origen:** archivo CSV versionado en el repositorio.
- **ETL:** Python + Pandas.
- **Almacenamiento:** PostgreSQL administrado (por ejemplo, Neon).
- **Automatización:** GitHub Actions, ejecución manual, al hacer push de cambios relevantes y programación diaria.
- **Visualización:** Streamlit Community Cloud.

## 2. Estructura

```text
sales-data-pipeline/
├── .github/workflows/etl.yml
├── data/sales_demo.csv
├── docs/
│   ├── article_medium.md
│   └── video_script.md
├── src/sales_pipeline/
│   ├── __init__.py
│   ├── config.py
│   ├── etl.py
│   └── main.py
├── tests/test_etl.py
├── .env.example
├── .gitignore
├── app.py
├── pytest.ini
├── README.md
└── requirements.txt
```

## 3. Requisitos previos

- Python 3.11.
- Git.
- Cuenta de GitHub.
- Una base PostgreSQL accesible desde Internet (Neon es una alternativa SaaS; también puedes usar otro proveedor PostgreSQL).
- Cuenta de Streamlit Community Cloud.

## 4. Ejecución local en Windows

Abre PowerShell en la carpeta del proyecto:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activación, usa Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Crea una base de datos PostgreSQL en tu proveedor. Copia `.env.example` como `.env` y reemplaza `DATABASE_URL` por la cadena real:

```powershell
Copy-Item .env.example .env
```

Ejemplo de formato (no uses literalmente estas credenciales):

```text
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_db?sslmode=require
```

No compartas ni subas `.env` a GitHub. La tabla `sales` se crea automáticamente durante la primera carga.

Ejecuta las pruebas:

```powershell
pytest -q
```

Ejecuta el ETL:

```powershell
$env:PYTHONPATH="src"
python -m sales_pipeline.main
```

En Git Bash:

```bash
export PYTHONPATH=src
python -m sales_pipeline.main
```

Inicia el dashboard:

```powershell
streamlit run app.py
```

Abre la dirección local que Streamlit muestre en la terminal.

## 5. PostgreSQL administrado con Neon (ejemplo)

1. Crea una cuenta en Neon y un proyecto PostgreSQL.
2. En el panel del proyecto, copia la cadena de conexión para Python/psycopg2.
3. Comprueba que la cadena incluya el host, base de datos, usuario y contraseña.
4. Para conexiones remotas, conserva `sslmode=require` si el proveedor lo indica.
5. Guarda la cadena en `.env` local y, posteriormente, como secreto de GitHub y Streamlit.

Los nombres y pantallas del proveedor pueden cambiar. Usa siempre la cadena de conexión que entregue tu panel; no publiques sus credenciales.

## 6. Publicar en GitHub

Crea un repositorio público llamado `sales-data-pipeline` en GitHub, sin inicializarlo con README si ya tienes este proyecto local.

Desde PowerShell, dentro de la carpeta:

```powershell
git init
git add .
git commit -m "Initial commit: Sales Data Pipeline"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sales-data-pipeline.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu usuario real de GitHub. Verifica que el repositorio sea público y que `.env` no aparezca en los archivos.

## 7. Configurar GitHub Actions

En GitHub:
1. Abre el repositorio → **Settings** → **Secrets and variables** → **Actions**.
2. Selecciona **New repository secret**.
3. Nombre: `DATABASE_URL`.
4. Valor: pega la cadena PostgreSQL completa.
5. Guarda.

El workflow `.github/workflows/etl.yml` se ejecuta al hacer push de cambios en `data/` o `src/`, manualmente desde **Actions → Sales ETL Pipeline → Run workflow**, y diariamente a las 06:00 UTC. GitHub Actions usa UTC; 06:00 UTC equivale a 01:00 en Perú.

En la pestaña **Actions**, abre la ejecución y confirma que los pasos de pruebas y ETL terminen correctamente. No declares automatización comprobada hasta tener una ejecución exitosa real.

## 8. Desplegar Streamlit Community Cloud

1. Asegúrate de que el repositorio esté en GitHub.
2. Entra a https://share.streamlit.io/ e inicia sesión con GitHub.
3. Selecciona **Create app** y el repositorio `sales-data-pipeline`.
4. Rama: `main`; archivo principal: `app.py`.
5. En la configuración avanzada de la aplicación, agrega el secreto:

```toml
DATABASE_URL = "postgresql://neondb_owner:npg_5Wl0OVMSEYTX@ep-calm-sound-be4rr0al-pooler.c-9.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

6. Despliega y espera a que finalice la instalación.
7. Abre la URL pública. Debe existir al menos una carga ETL correcta para que el dashboard muestre información.

La URL de Streamlit será asignada por la plataforma; agrégala al artículo y al README cuando exista.

## 9. Pruebas y validación

- `pytest -q`: comprueba reglas de limpieza, deduplicación y cálculo de ingresos.
- ETL local: confirma conexión y carga a PostgreSQL.
- GitHub Actions: confirma automatización en la nube.
- Streamlit: confirma lectura de PostgreSQL, métricas, filtros y gráficos.

La carga usa `sale_id` como clave primaria y hace *upsert*: ejecutar el pipeline repetidamente no duplica las ventas existentes. Si un registro con el mismo ID cambia, se actualiza.

## 10. Seguridad

- Nunca subas `.env`, contraseñas ni cadenas de conexión.
- Usa GitHub Actions Secrets y Streamlit Secrets.
- Usa TLS/SSL en conexiones remotas según los requisitos del proveedor.
- Para una aplicación real, limita permisos del usuario de base de datos y evita credenciales administrativas.
- Rota las credenciales si se exponen accidentalmente.

## 11. Limitaciones conocidas

- La fuente es un CSV estático de demostración; el workflow diario vuelve a procesar ese mismo archivo.
- No hay ingestión incremental desde un sistema de ventas real.
- El proyecto no incorpora orquestadores complejos ni infraestructura de AWS.
- Los resultados son demostrativos y dependen del contenido del CSV y de la base cargada.


