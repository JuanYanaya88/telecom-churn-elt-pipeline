"""Extraccion de datos de la API Telecom X y carga al schema raw de Postgres."""
import json
import os

import pandas as pd
import requests
from sqlalchemy import create_engine

API_URL = os.getenv(
    "TELECOM_API_URL",
    "https://raw.githubusercontent.com/ingridcristh/challenge2-data-science-LATAM/main/TelecomX_Data.json",
)
WAREHOUSE_CONN = os.getenv(
    "WAREHOUSE_CONN", "postgresql://warehouse:warehouse@localhost:5432/warehouse"
)


def extract() -> pd.DataFrame:
    """Descarga el JSON de la API y lo aplana a un DataFrame."""
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return pd.json_normalize(data, sep="_")


def load(df: pd.DataFrame) -> int:
    """Carga el DataFrame al schema raw (reemplazo completo, idempotente)."""
    engine = create_engine(WAREHOUSE_CONN)
    df.to_sql("customers", engine, schema="raw", if_exists="replace", index=False)
    return len(df)


def run() -> None:
    df = extract()
    rows = load(df)
    print(f"Cargadas {rows} filas en raw.customers")


if __name__ == "__main__":
    run()
