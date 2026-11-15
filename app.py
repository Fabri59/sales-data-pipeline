import os
from pathlib import Path
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

st.set_page_config(page_title="Sales Data Pipeline", page_icon="📊", layout="wide")
st.title("📊 Sales Data Pipeline")
st.caption("Dashboard demostrativo de análisis comercial alimentado por PostgreSQL.")

@st.cache_resource
def get_engine():
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        try:
            url = str(st.secrets["DATABASE_URL"]).strip()
        except (FileNotFoundError, KeyError):
            url = ""
    if not url:
        raise RuntimeError("Configura DATABASE_URL en los Secrets de Streamlit.")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://") and "+" not in url.split("://", 1)[0]:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return create_engine(url, pool_pre_ping=True)

@st.cache_data(ttl=60)
def load_data():
    query = """
        SELECT sale_id, sale_date, product, category, quantity,
               unit_price, discount_rate, revenue
        FROM sales ORDER BY sale_date
    """
    with get_engine().connect() as conn:
        df = pd.read_sql(text(query), conn)
    if not df.empty:
        df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df

try:
    data = load_data()
except Exception as exc:
    st.error(f"No se pudo consultar PostgreSQL: {exc}")
    st.info("Verifica que DATABASE_URL esté configurada y que el pipeline ya haya cargado datos.")
    st.stop()

if data.empty:
    st.warning("La tabla sales todavía no contiene registros. Ejecuta el pipeline ETL.")
    st.stop()

with st.sidebar:
    st.header("Filtros")
    min_date, max_date = data["sale_date"].min().date(), data["sale_date"].max().date()
    date_range = st.date_input("Periodo", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    categories = sorted(data["category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Categorías", categories, default=categories)
    products = sorted(data["product"].dropna().unique().tolist())
    selected_products = st.multiselect("Productos", products, default=products)
    if st.button("Actualizar datos"):
        st.cache_data.clear()
        st.rerun()

filtered = data.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        filtered["sale_date"].dt.date.between(date_range[0], date_range[1])
    ]
if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]
else:
    filtered = filtered.iloc[0:0]
if selected_products:
    filtered = filtered[filtered["product"].isin(selected_products)]
else:
    filtered = filtered.iloc[0:0]

revenue = float(filtered["revenue"].sum())
sales_count = int(filtered["sale_id"].nunique())
units = int(filtered["quantity"].sum())
average = revenue / sales_count if sales_count else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ingresos totales", f"S/ {revenue:,.2f}")
c2.metric("Cantidad de ventas", f"{sales_count:,}")
c3.metric("Unidades vendidas", f"{units:,}")
c4.metric("Ticket promedio", f"S/ {average:,.2f}")

left, right = st.columns(2)
with left:
    st.subheader("Ingresos por mes")
    monthly = filtered.assign(month=filtered["sale_date"].dt.to_period("M").astype(str))
    monthly_chart = monthly.groupby("month", as_index=False)["revenue"].sum()
    if not monthly_chart.empty:
        st.bar_chart(monthly_chart.set_index("month")["revenue"])
    else:
        st.info("No hay datos para los filtros seleccionados.")
with right:
    st.subheader("Ingresos por categoría")
    category_chart = filtered.groupby("category")["revenue"].sum().sort_values(ascending=False)
    if not category_chart.empty:
        st.bar_chart(category_chart)
    else:
        st.info("No hay datos para los filtros seleccionados.")

st.subheader("Productos más vendidos")
top_products = (
    filtered.groupby("product", as_index=False)["quantity"].sum()
    .sort_values("quantity", ascending=False).head(10)
)
if not top_products.empty:
    st.bar_chart(top_products.set_index("product")["quantity"])
else:
    st.info("No hay datos para los filtros seleccionados.")

with st.expander("Consultar registros procesados"):
    st.dataframe(filtered.sort_values("sale_date", ascending=False), use_container_width=True)
    st.download_button(
        "Descargar vista filtrada (CSV)",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="sales_filtered.csv",
        mime="text/csv"
    )
st.caption("Fuente: dataset sintético de demostración. No representa ventas reales.")
