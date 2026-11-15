from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, MetaData

REQUIRED_COLUMNS = [
    "sale_id", "sale_date", "product", "category",
    "quantity", "unit_price", "discount_rate"
]

def extract(csv_path: str | Path) -> pd.DataFrame:
    """Lee el CSV de origen y valida que contenga las columnas esperadas."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV: {path}")
    df = pd.read_csv(path)
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Faltan columnas obligatorias en el CSV: {missing}")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia, tipa y enriquece los registros de ventas."""
    data = df.copy()
    data = data[REQUIRED_COLUMNS]

    data["sale_id"] = data["sale_id"].astype("string").str.strip()
    data["product"] = data["product"].astype("string").str.strip()
    data["category"] = data["category"].astype("string").str.strip()
    data["sale_date"] = pd.to_datetime(data["sale_date"], errors="coerce").dt.date
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    data["discount_rate"] = pd.to_numeric(data["discount_rate"], errors="coerce")

    # Un identificador, fecha, producto, cantidad y precio válidos son indispensables.
    data = data.dropna(subset=[
        "sale_id", "sale_date", "product", "quantity", "unit_price"
    ])
    data = data[
        (data["sale_id"] != "") &
        (data["product"] != "") &
        (data["quantity"] > 0) &
        (data["unit_price"] >= 0)
    ].copy()

    data["category"] = data["category"].fillna("Sin categoría").replace("", "Sin categoría")
    data["discount_rate"] = data["discount_rate"].fillna(0).clip(0, 1)
    data["quantity"] = data["quantity"].astype(int)
    data["unit_price"] = data["unit_price"].round(2)
    data["discount_rate"] = data["discount_rate"].round(4)

    # Si el ID aparece varias veces, se conserva la última aparición del archivo.
    data = data.drop_duplicates(subset=["sale_id"], keep="last")
    data["revenue"] = (
        data["quantity"] * data["unit_price"] * (1 - data["discount_rate"])
    ).round(2)
    return data.sort_values(["sale_date", "sale_id"]).reset_index(drop=True)

def load_to_postgres(df: pd.DataFrame, database_url: str) -> int:
    """Crea la tabla si no existe e inserta/actualiza por sale_id (carga idempotente)."""
    if df.empty:
        return 0

    engine = create_engine(database_url, pool_pre_ping=True)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        sale_id VARCHAR(80) PRIMARY KEY,
        sale_date DATE NOT NULL,
        product VARCHAR(160) NOT NULL,
        category VARCHAR(120) NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
        discount_rate NUMERIC(6,4) NOT NULL CHECK (discount_rate >= 0 AND discount_rate <= 1),
        revenue NUMERIC(14,2) NOT NULL,
        loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_sales_sale_date ON sales(sale_date);
    CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category);
    """
    records = df.copy()
    records["sale_date"] = records["sale_date"].astype(str)
    rows = records.to_dict(orient="records")

    with engine.begin() as conn:
        for statement in create_table_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement))
        metadata = MetaData()
        sales = Table("sales", metadata, autoload_with=conn)
        stmt = insert(sales).values(rows)
        update_columns = {
            col.name: getattr(stmt.excluded, col.name)
            for col in sales.columns
            if col.name not in ("sale_id", "loaded_at")
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=["sale_id"],
            set_=update_columns
        )
        conn.execute(stmt)
    engine.dispose()
    return len(rows)
