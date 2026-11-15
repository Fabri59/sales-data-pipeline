import argparse
import logging
from pathlib import Path
from .config import PROJECT_ROOT, get_database_url
from .etl import extract, transform, load_to_postgres

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

def run_pipeline(csv_path: str | Path | None = None) -> dict:
    source = Path(csv_path) if csv_path else PROJECT_ROOT / "data" / "sales_demo.csv"
    logger.info("Iniciando pipeline. Fuente: %s", source)
    raw = extract(source)
    clean = transform(raw)
    loaded = load_to_postgres(clean, get_database_url())
    result = {
        "source_rows": len(raw),
        "clean_rows": len(clean),
        "loaded_rows": loaded,
        "rejected_or_removed_rows": len(raw) - len(clean),
    }
    logger.info("Pipeline finalizado: %s", result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ETL de ventas")
    parser.add_argument("--csv", default=None, help="Ruta opcional al CSV")
    args = parser.parse_args()
    run_pipeline(args.csv)
