import pandas as pd
from sales_pipeline.etl import transform

def test_transform_removes_duplicates_and_calculates_revenue():
    raw = pd.DataFrame([
        {"sale_id":"A1","sale_date":"2026-01-02","product":"Teclado","category":"Accesorios",
         "quantity":"2","unit_price":"50","discount_rate":"0.10"},
        {"sale_id":"A1","sale_date":"2026-01-02","product":"Teclado","category":"Accesorios",
         "quantity":"2","unit_price":"50","discount_rate":"0.10"},
        {"sale_id":"A2","sale_date":"fecha-invalida","product":"Mouse","category":"Accesorios",
         "quantity":"1","unit_price":"25","discount_rate":""},
        {"sale_id":"A3","sale_date":"2026-01-03","product":"Monitor","category":"",
         "quantity":"1","unit_price":"500","discount_rate":""},
    ])
    result = transform(raw)
    assert len(result) == 2
    assert result.loc[result.sale_id == "A1", "revenue"].iloc[0] == 90
    assert result.loc[result.sale_id == "A3", "category"].iloc[0] == "Sin categoría"
    assert result["sale_id"].is_unique

def test_transform_returns_empty_for_invalid_rows():
    raw = pd.DataFrame([
        {"sale_id":"","sale_date":"2026-01-01","product":"X","category":"A",
         "quantity":1,"unit_price":10,"discount_rate":0}
    ])
    assert transform(raw).empty
